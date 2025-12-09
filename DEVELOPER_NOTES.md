# OpenStudio MCP Server - Developer Notes

## How the Server Works

### Architecture Overview

```
User (in Claude Desktop)
    ↓
Claude AI Assistant
    ↓
MCP Protocol (stdin/stdout JSON-RPC)
    ↓
FastMCP Server (server.py)
    ↓
OpenStudioManager (openstudio_manager.py)
    ↓
OpenStudio Toolkit (openstudio_toolkit library)
    ↓
OpenStudio SDK (C++ library with Python bindings)
```

### Component Responsibilities

1. **server.py** - MCP tool definitions
   - Defines all MCP tools with `@mcp.tool()` decorator
   - Handles parameter validation
   - Converts results to JSON strings
   - Returns errors in consistent format

2. **openstudio_manager.py** - Business logic layer
   - Maintains state (current_model, current_file_path)
   - Wraps OpenStudio Toolkit functions
   - Converts Python objects to JSON-serializable dicts
   - Provides error handling and logging

3. **openstudio_toolkit** - OpenStudio operations
   - Your library with domain-specific functions
   - Uses OpenStudio SDK directly
   - Returns pandas DataFrames and OpenStudio objects

4. **config.py** - Configuration management
   - Auto-detects OpenStudio installation
   - Manages file paths (workspace, sample_files, outputs)
   - Sets up logging

## Typical User Flow

### Scenario 1: User Loads and Analyzes a Model

**User message**: "Load R2F-Office-Hub-006.osm and tell me about the spaces"

**Claude's internal process**:

1. **Recognizes task**: Need to load model and get space information

2. **Tool selection**:
   - `load_osm_model` (to load the file)
   - `list_spaces` (to get space data)

3. **Execution sequence**:

   **Step 1: load_osm_model**
   ```
   Claude calls: load_osm_model("R2F-Office-Hub-006.osm")

   server.py receives:
   {
     "tool": "load_osm_model",
     "arguments": {
       "file_path": "R2F-Office-Hub-006.osm",
       "translate_version": true
     }
   }

   server.py:load_osm_model() executes:
   - Logs the call
   - Calls os_manager.load_osm_file("R2F-Office-Hub-006.osm", True)

   openstudio_manager.py:load_osm_file() executes:
   - Calls resolve_osm_path(config, "R2F-Office-Hub-006.osm")
     → Searches workspace, sample_files, models directories
     → Finds: /workspace/sample_files/models/R2F-Office-Hub-006.osm

   - Checks if file exists (os.path.exists)
     → Returns True

   - Calls OpenStudio Toolkit:
     from openstudio_toolkit.utils.osm_utils import load_osm_file_as_model
     model = load_osm_file_as_model(resolved_path, translate_version=True)

   - OpenStudio Toolkit:
     → Uses openstudio.model.Model.load(file_path)
     → Optionally translates to current version
     → Returns OpenStudio Model object

   - Updates state:
     self.current_model = model
     self.current_file_path = resolved_path

   - Gets building info:
     building_info = self._get_building_summary()
     → Calls openstudio_toolkit.osm_objects.building.get_building_object_as_dataframe
     → Returns DataFrame with building properties
     → Converts to dict

   - Returns success dict:
     {
       "status": "success",
       "message": "Successfully loaded OSM file: R2F-Office-Hub-006.osm",
       "file_path": "/workspace/sample_files/models/R2F-Office-Hub-006.osm",
       "model_info": {
         "name": "R2F-Office-Hub-006",
         "floor_area": 1234.5,
         ...
       }
     }

   server.py converts to JSON string and returns to Claude
   ```

   **Step 2: list_spaces**
   ```
   Claude calls: list_spaces()

   server.py receives:
   {
     "tool": "list_spaces",
     "arguments": {}
   }

   server.py:list_spaces() executes:
   - Calls os_manager.get_all_spaces()

   openstudio_manager.py:get_all_spaces() executes:
   - Checks: self._check_model_loaded()
     → Raises ValueError if self.current_model is None

   - Calls OpenStudio Toolkit:
     from openstudio_toolkit.osm_objects.spaces import get_all_space_objects_as_dataframe
     df = get_all_space_objects_as_dataframe(self.current_model)

   - OpenStudio Toolkit:
     → Iterates through model.getSpaces()
     → Extracts properties: name, floor_area, thermal_zone, etc.
     → Returns pandas DataFrame

   - Converts DataFrame to list of dicts:
     spaces = df.to_dict(orient='records')

   - Returns:
     {
       "status": "success",
       "count": 12,
       "spaces": [
         {"name": "Space 1", "floor_area": 100, ...},
         {"name": "Space 2", "floor_area": 150, ...},
         ...
       ]
     }

   server.py converts to JSON string and returns
   ```

4. **Claude interprets results**:
   - Reads the JSON responses
   - Extracts key information (12 spaces, names, areas)
   - Composes natural language response

5. **Claude responds to user**:
   "I've loaded the model R2F-Office-Hub-006.osm. It contains 12 spaces with a total floor area of 1,234 m². The spaces include..."

### Scenario 2: User Converts to IDF

**User message**: "Convert this model to EnergyPlus format"

**Claude's process**:

1. **Tool selection**: `convert_to_idf`

2. **Execution**:
   ```
   Claude calls: convert_to_idf()

   server.py:convert_to_idf() executes:
   - Calls os_manager.convert_to_idf(output_path=None)

   openstudio_manager.py:convert_to_idf() executes:
   - Checks model loaded

   - Generates output path:
     If output_path is None:
       base_name = "R2F-Office-Hub-006"  # from current_file_path
       output_path = "/workspace/outputs/R2F-Office-Hub-006.idf"

   - Calls OpenStudio Toolkit:
     from openstudio_toolkit.utils.osm_utils import convert_osm_to_idf
     convert_osm_to_idf(self.current_model, output_path)

   - OpenStudio Toolkit:
     → Uses OpenStudio ForwardTranslator
     → Converts OSM objects to IDF format
     → Writes IDF file

   - Returns:
     {
       "status": "success",
       "message": "Successfully converted to IDF: R2F-Office-Hub-006.idf",
       "file_path": "/workspace/outputs/R2F-Office-Hub-006.idf"
     }
   ```

3. **Claude responds**:
   "I've converted the model to EnergyPlus IDF format. The file is saved at outputs/R2F-Office-Hub-006.idf"

## What Each Tool Returns

### File Operations

**load_osm_model**
```json
{
  "status": "success",
  "message": "Successfully loaded OSM file: model.osm",
  "file_path": "/workspace/sample_files/models/model.osm",
  "model_info": {
    "name": "Building Name",
    "floor_area": 1234.5,
    "number_of_stories": 3
  }
}
```

**save_osm_model**
```json
{
  "status": "success",
  "message": "Successfully saved OSM file: model.osm",
  "file_path": "/workspace/outputs/model.osm"
}
```

**convert_to_idf**
```json
{
  "status": "success",
  "message": "Successfully converted to IDF: model.idf",
  "file_path": "/workspace/outputs/model.idf"
}
```

**copy_file**
```json
{
  "status": "success",
  "message": "Successfully copied file",
  "source": {
    "original_path": "source.osm",
    "resolved_path": "/workspace/sample_files/models/source.osm",
    "size_bytes": 12345
  },
  "target": {
    "original_path": "target.osm",
    "resolved_path": "/workspace/outputs/target.osm",
    "size_bytes": 12345
  },
  "copy_duration_seconds": 0.05
}
```

### Information Retrieval

**get_model_summary**
```json
{
  "status": "success",
  "model_loaded": true,
  "file_path": "/workspace/sample_files/models/model.osm",
  "building": {
    "name": "Building Name",
    "floor_area": 1234.5
  },
  "counts": {
    "spaces": 12,
    "thermal_zones": 4,
    "surfaces": 68
  }
}
```

**list_spaces**
```json
{
  "status": "success",
  "count": 12,
  "spaces": [
    {
      "name": "Space 1",
      "floor_area": 100.5,
      "volume": 350.0,
      "thermal_zone": "Zone 1"
    },
    ...
  ]
}
```

**list_thermal_zones**
```json
{
  "status": "success",
  "count": 4,
  "thermal_zones": [
    {
      "name": "Zone 1",
      "multiplier": 1,
      "spaces_count": 3
    },
    ...
  ]
}
```

**list_materials**
```json
{
  "status": "success",
  "count": 25,
  "materials": [
    {
      "name": "Concrete",
      "thickness": 0.2,
      "conductivity": 1.8,
      "density": 2400,
      "specific_heat": 840
    },
    ...
  ]
}
```

### Error Responses

All tools return errors in this format:
```json
{
  "status": "error",
  "error": "Detailed error message here"
}
```

Common errors:
- "No model loaded. Load a model first."
- "OSM file not found: /path/to/file.osm"
- "Failed to load OSM file: Invalid format"

## Bugs That Were Fixed

### Bug 1: Wrong workspace_root in Docker

**Problem**: Config had wrong workspace_root
```python
workspace_root: str = "/workspace/openstudio-mcp-server"  # Wrong!
```

**But Docker mounts to**: `-v C:\openstudio-mcp-server:/workspace`

**Fix**: Changed config.py:
```python
workspace_root: str = "/workspace"  # Correct!
```

### Bug 2: Claude Desktop Can't Find Uploaded Files (FIXED - Critical)

**Problem**: Path resolution was broken due to incorrect directory handling:
- Added directories to search paths WITHOUT checking if they exist
- Stored full file paths instead of base directories
- Did not follow EnergyPlus MCP proven pattern

**Root Cause**: Code was doing this:
```python
# WRONG - builds full path immediately, doesn't check dir exists
search_paths.append(("Claude uploads", os.path.join("/mnt/user-data/uploads", file_path)))

# Then tried to check if FULL PATH exists (wrong!)
for location, path in search_paths:
    if os.path.exists(path):  # This checks file, not directory!
```

**Fix Applied** (following EnergyPlus MCP pattern):
```python
# CORRECT - only add directory if it exists
if os.path.exists("/mnt/user-data/uploads"):
    search_paths.append(("Claude uploads", "/mnt/user-data/uploads"))

# Then build candidate path and check
for location, search_dir in search_paths:
    candidate_path = os.path.join(search_dir, file_path)
    if os.path.exists(candidate_path):
        return os.path.abspath(candidate_path)
```

**Key Changes**:
1. Check if base directory exists BEFORE adding to search paths
2. Store only the base directory, not the full file path
3. Build candidate path inside the loop
4. Return absolute path for consistency

**Result**: Server now works in **both environments**:
- Docker: Uses `/workspace/` paths ✓
- Claude Desktop: Uses `/mnt/user-data/uploads/` and `/home/claude/` ✓
- Dynamic discovery: Only searches directories that actually exist ✓

## How Claude Should Use the Tools

### Pattern 1: Load and Analyze

```
User: "Analyze building.osm"

Claude should:
1. load_osm_model("building.osm")
2. get_model_summary()
3. list_spaces()
4. list_thermal_zones()
5. Summarize findings in natural language
```

### Pattern 2: Specific Query

```
User: "What materials are used?"

Claude should:
1. Check if model is loaded (may need to load first)
2. list_materials()
3. Present the materials list
```

### Pattern 3: Export

```
User: "Export to EnergyPlus"

Claude should:
1. Check if model is loaded
2. convert_to_idf()
3. Confirm the output file location
```

### Pattern 4: Compare Models

```
User: "Compare model1.osm and model2.osm"

Claude should:
1. load_osm_model("model1.osm")
2. get_model_summary() → save results
3. list_spaces() → save results
4. load_osm_model("model2.osm")
5. get_model_summary() → compare with saved
6. list_spaces() → compare with saved
7. Present comparison
```

## Common Issues and Solutions

### Issue: "No module named 'openstudio_toolkit'"

**Cause**: Toolkit not installed or not in Python path

**Solution**:
- Manual install: Copy `openstudio_toolkit/` to project root
- Or: Install from git in pyproject.toml (requires git in Docker)

### Issue: "Model not loaded" error

**Cause**: Claude tries to use inspection tools without loading model first

**Solution**: Claude should always load model first or check `get_current_model_status`

### Issue: "File not found" even though file exists

**Cause**:
1. Wrong workspace_root (fixed now)
2. File not in mounted volume
3. Permission issues

**Solution**: Check Docker mount, verify paths

### Issue: Tools return empty results

**Cause**: Model is valid but has no objects of that type

**Example**: `list_air_loops()` returns `{"count": 0, "air_loops": []}` if model has no HVAC systems

**Solution**: This is correct behavior, Claude should handle gracefully

## Testing the Server

### Quick Test

```bash
docker run --rm -i \
  -v "C:\openstudio-mcp-server:/workspace" \
  openstudio-mcp-dev bash -c "
  cd /workspace && uv run python -c '
from openstudio_mcp_server import OpenStudioManager, get_config
import os

config = get_config()
manager = OpenStudioManager(config)

# Test file exists
test_file = os.path.join(config.paths.sample_files_path, \"models\", \"R2F-Office-Hub-006.osm\")
print(f\"File exists: {os.path.exists(test_file)}\")

# Test load
result = manager.load_osm_file(test_file)
print(f\"Load status: {result[\"status\"]}\")

# Test get spaces
spaces = manager.get_all_spaces()
print(f\"Spaces count: {spaces[\"count\"]}\")
'
"
```

Expected output:
```
File exists: True
Load status: success
Spaces count: 12
```

## Critical Fixes & Architectural Decisions

### JSON Serialization Fix (December 2024)

**Problem: `SyntaxError: Unexpected token 'u'` in Claude Desktop**

Users reported a JSON parsing error when using the server with Claude Desktop:
```
SyntaxError: Unexpected token 'u', "[utilities"... is not valid JSON
```

**Root Cause:**
The error occurred when Python objects (lists or dicts) were accidentally converted to strings using Python's `str()` function instead of proper JSON serialization. This created invalid JSON with single quotes:
```python
# WRONG - Python representation
str(['item1', 'item2'])  # → "['item1', 'item2']"  (single quotes - invalid JSON)

# CORRECT - JSON serialization
json.dumps(['item1', 'item2'])  # → '["item1", "item2"]'  (double quotes - valid JSON)
```

**Solution: `ensure_json_response()` Wrapper**

Created a defensive wrapper function in `utils/json_utils.py`:

```python
def ensure_json_response(result: Any) -> str:
    """Ensures all responses are properly JSON-serialized."""
    try:
        if isinstance(result, str):
            try:
                json.loads(result)  # Validate it's already JSON
                return result
            except json.JSONDecodeError:
                # Wrap plain strings in a structured response
                return json.dumps({"status": "success", "message": result}, indent=2)

        # Serialize all other types (dict, list, etc.)
        return json.dumps(result, indent=2, default=str)

    except Exception as e:
        # Safe fallback - no recursion
        return json.dumps({"status": "error", "error": f"Serialization error: {str(e)}"}, indent=2)
```

**Key Features:**
1. **Validates existing JSON strings** - Checks if a string is already valid JSON
2. **Wraps plain messages** - Converts simple strings to structured responses
3. **Handles edge cases** - Uses `default=str` to serialize non-standard objects
4. **Safe error handling** - Returns simple error dict if serialization fails (no recursion)

**Recursion Bug Fix:**

Initial implementation had a critical bug where the error handler called itself recursively:
```python
# BUG - Infinite recursion
except Exception as e:
    return ensure_json_response({"error": str(e)})  # ← Calls itself again!
```

**Fixed version:**
```python
# FIXED - Direct serialization
except Exception as e:
    return json.dumps({"status": "error", "error": str(e)}, indent=2)  # ← Safe
```

**Applied to All Tools:**
- All 19+ MCP tools now use `ensure_json_response()` for their return values
- Both success and error paths are protected
- Located in: `openstudio_mcp_server/utils/json_utils.py`
- Imported in: `openstudio_mcp_server/server.py`

---

### Docker Volume Mapping Architecture

**Challenge: File Access in Isolated Containers**

The MCP server runs inside a Docker container with an isolated filesystem. To read/write files on the host machine (user's computer), we must use Docker volume mounts.

**Solution: Dual Volume Mount Strategy**

The Claude Desktop configuration uses **two separate volume mounts**:

```json
{
  "mcpServers": {
    "openstudio": {
      "command": "docker",
      "args": [
        "-v", "C:\\:/mnt/c",                    // Mount 1: Host C: drive access
        "-v", "C:\\path\\to\\repo:/workspace"  // Mount 2: Server source code
      ]
    }
  }
}
```

**Mount 1: C: Drive Access (`-v C:\:/mnt/c`)**

**Purpose:** Grants the server READ/WRITE access to the user's entire C: drive.

**Mapping:**
```
Host (Windows)                     Container (Linux)
─────────────────                  ─────────────────
C:\Users\Name\Downloads\    →     /mnt/c/Users/Name/Downloads/
C:\Users\Name\Documents\    →     /mnt/c/Users/Name/Documents/
C:\Projects\                →     /mnt/c/Projects/
```

**Why Critical:**
- Enables `load_osm_model` to read user-uploaded files
- Enables `save_osm_model` to write outputs that persist on host
- Enables `convert_to_idf` to export IDF files to user directories
- Without this mount, files saved inside the container disappear when it stops

**Mount 2: Server Source Code (`-v repo:/workspace`)**

**Purpose:** Mounts the cloned repository into the container at `/workspace`.

**Why Needed:**
- Container needs access to Python source code
- Enables live code changes during development
- Provides access to sample files and test models
- Sets the working directory for `uv run` command

**Path Resolution Strategy:**

The server implements intelligent path resolution (in `utils/path_utils.py`):

1. **Absolute paths starting with `/mnt/c`** - Direct host file access
2. **Relative paths** - Searched in priority order:
   - `/mnt/user-data/uploads` (Claude Desktop uploads)
   - `/home/claude` (Claude working directory)
   - `/workspace/sample_files/models` (Project samples)
   - `/workspace/sample_files`
   - `/workspace/outputs`
   - `/workspace`

**Example User Flow:**
```
User: "Load /mnt/c/Users/John/Downloads/model.osm"
  ↓
Server: resolve_path() recognizes absolute path
  ↓
Server: Reads file directly from /mnt/c/Users/John/Downloads/model.osm
  ↓
Success: File loaded from user's actual Downloads folder
```

**Testing the Mounts:**

The only reliable way to verify volume mounts work is using MCP Inspector with Docker:

```bash
npx @modelcontextprotocol/inspector docker run --rm -i \
  -v "C:\:/mnt/c" \
  -v "$(pwd):/workspace" \
  -w "/workspace/openstudio-mcp-server" \
  openstudio-mcp-dev \
  uv run openstudio_mcp_server/server.py
```

See `TESTING_PROTOCOL.md` → "How to Debug Docker Volumes" for comprehensive testing instructions.

---

### Parameter Mismatch Bug Fix (save_osm_model)

**Problem:** `TypeError: save_model_as_osm_file() got unexpected keyword argument 'file_path'`

**Root Cause:**
The `openstudio_tools.py` was calling toolkit function with wrong parameter name:
```python
# BUG in openstudio_tools.py (line 149)
save_model_as_osm_file(
    osm_model=self.current_model,
    file_path=save_path  # ← WRONG parameter name
)
```

**Fix:**
```python
# FIXED
save_model_as_osm_file(
    osm_model=self.current_model,
    osm_file_path=save_path  # ← Correct parameter name
)
```

**Lesson Learned:**
Always verify the exact parameter names of wrapped functions. Consider using `**kwargs` for flexibility or explicit parameter matching.

---

## Next Steps for Development

### Priority Fixes
1. ✓ Fix workspace_root path (DONE)
2. ✓ Install OpenStudio Python package in Dockerfile (DONE)
3. Test all tools with the actual model file
4. Add validation for tool parameters

### Future Enhancements
1. Add more modification tools (create spaces, zones, etc.)
2. Add simulation execution tools
3. Add results parsing tools
4. Add geometry creation tools
5. Add schedule creation/modification tools

### Testing Recommendations
1. Create unit tests for each tool
2. Test with various model sizes
3. Test error conditions
4. Test with invalid inputs
5. Performance testing with large models

---

**Current Status**: Server should now work correctly. The workspace_root fix resolves the "file not found" issue.
