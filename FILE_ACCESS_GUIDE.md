# File Access Guide

## Overview

The OpenStudio MCP Server can automatically find your model files even if you don't provide the full path. It searches multiple locations and can even match partial file names.

This guide explains how file discovery works when you ask Claude to load or work with your models.

---

## Problem: File Access in Docker Containers

When Claude Desktop uploads files, they are typically placed in locations like:
- `/mnt/user-data/uploads/` (Linux/macOS)
- `/home/claude/` (Linux)
- `C:\Users\username\AppData\Local\Temp\` (Windows)

However, the Docker container running the OpenStudio MCP Server only has access to the mounted workspace directory (typically `/workspace`). This means **uploaded files are not directly accessible** to the MCP tools.

---

## Solution: Intelligent Path Resolution + copy_file Tool

The OpenStudio MCP Server now provides two complementary solutions:

### 1. Intelligent Path Resolution

All file-loading tools (`load_osm_model`, etc.) now use **smart path resolution** that:

- **Searches multiple locations**:
  - Workspace root directory
  - Sample files directory (`sample_files/`)
  - Models subdirectory (`sample_files/models/`)
  - Output directory (`outputs/`)

- **Supports fuzzy matching**:
  - Finds files with partial names (e.g., "office" finds "OfficeBuilding.osm")
  - Tolerates typos and case differences
  - Suggests similar files when exact match isn't found

- **Flexible path formats**:
  - Absolute paths: `/full/path/to/model.osm`
  - Relative paths: `models/example.osm`
  - Filename only: `example.osm` (searches known directories)

### 2. copy_file Tool

The new `copy_file` tool helps move user-uploaded files into the workspace where other tools can access them.

**Key Features:**
- Intelligent source file discovery with fuzzy matching
- Automatic target directory creation
- File validation (size verification)
- Detailed error messages with suggestions
- Metadata preservation (timestamps, permissions)

---

## Usage Examples

### Example 1: Direct File Access (If File Is in Workspace)

```python
# If user has already placed file in workspace
load_osm_model("sample_files/models/example.osm")
```

### Example 2: Copy Then Load (For Uploaded Files)

```python
# Step 1: Copy uploaded file to workspace
copy_file(
    source_path="/mnt/user-data/uploads/MyBuilding.osm",
    target_path="workspace/MyBuilding.osm",
    file_types=[".osm"]
)

# Step 2: Load the copied file
load_osm_model("workspace/MyBuilding.osm")
```

### Example 3: Fuzzy Matching

```python
# User says "load the office model" but doesn't know exact filename
# The system will search for files with "office" in the name

# Option A: Direct load if file is in workspace
load_osm_model("office")  # Finds "OfficeBuilding.osm"

# Option B: Copy with fuzzy matching
copy_file(
    source_path="office",
    target_path="my_office.osm",
    file_types=[".osm"]
)
```

### Example 4: Handling Errors with Suggestions

```python
# If file not found, you get suggestions
load_osm_model("offce")  # Typo!

# Error response includes:
# "Did you mean one of these?
#  - /workspace/sample_files/models/OfficeBuilding.osm
#  - /workspace/sample_files/models/SmallOffice.osm"
```

---

## copy_file Tool Details

### Signature

```python
copy_file(
    source_path: str,
    target_path: str,
    overwrite: bool = False,
    file_types: Optional[List[str]] = None
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_path` | str | Source file path (can be absolute, relative, or fuzzy match) |
| `target_path` | str | Target file path (can be absolute, relative, or filename only) |
| `overwrite` | bool | Whether to overwrite existing target (default: False) |
| `file_types` | list | Valid file extensions, e.g., `[".osm", ".idf"]` (optional) |

### Return Value

Returns JSON with detailed information:

**Success:**
```json
{
  "status": "success",
  "message": "Successfully copied file",
  "source": {
    "original_path": "/mnt/user-data/uploads/model.osm",
    "resolved_path": "/mnt/user-data/uploads/model.osm",
    "size_bytes": 12345
  },
  "target": {
    "original_path": "workspace/model.osm",
    "resolved_path": "/workspace/openstudio-mcp-server/workspace/model.osm",
    "size_bytes": 12345
  },
  "copy_duration_seconds": 0.05
}
```

**Error with Suggestions:**
```json
{
  "status": "error",
  "error": "source file not found: offce.osm\nDid you mean one of these?\n  - OfficeBuilding.osm\n  - SmallOffice.osm",
  "original_paths": {
    "source": "offce.osm",
    "target": "my_model.osm"
  }
}
```

---

## Path Resolution Algorithm

When you specify a file path, the system tries these strategies **in order**:

1. **Absolute Path**: If path starts with `/` or `C:\`, check directly
2. **Workspace Root**: Check `{workspace_root}/{file_path}`
3. **Sample Files**: Check `{workspace_root}/sample_files/{file_path}`
4. **Models Subdirectory**: Check `{workspace_root}/sample_files/models/{file_path}`
5. **Output Directory**: Check `{workspace_root}/outputs/{file_path}`
6. **Current Directory**: Check `./{file_path}`
7. **Fuzzy Matching** (if enabled): Search for similar filenames using `difflib.SequenceMatcher`

### Fuzzy Matching

The fuzzy matching algorithm:
- Walks through all search directories
- Compares filenames using sequence matching (30% similarity threshold)
- Ranks results by similarity score
- Returns top 10 suggestions

**Example:**
- Search for: `"offce"` (typo)
- Finds: `"OfficeBuilding.osm"` (80% similarity)
- Suggests: `"SmallOffice.osm"` (70% similarity)

---

## Configuration for Claude Desktop

To give the MCP server access to uploaded files, you need to mount additional directories.

### Current Configuration (Limited Access)

```json
{
  "mcpServers": {
    "openstudio": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "C:\\openstudio-mcp-server:/workspace",
        "-w", "/workspace/openstudio-mcp-server",
        "openstudio-mcp-dev",
        "uv", "run", "python", "-m", "openstudio_mcp_server.server"
      ]
    }
  }
}
```

### Enhanced Configuration (Better File Access)

**Option A: Mount User Home Directory** (macOS/Linux)
```json
{
  "mcpServers": {
    "openstudio": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "C:\\openstudio-mcp-server:/workspace",
        "-v", "/home/username:/user-home:ro",
        "-w", "/workspace/openstudio-mcp-server",
        "openstudio-mcp-dev",
        "uv", "run", "python", "-m", "openstudio_mcp_server.server"
      ]
    }
  }
}
```

**Option B: Mount Specific Upload Directory** (if known)
```json
{
  "mcpServers": {
    "openstudio": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "C:\\openstudio-mcp-server:/workspace",
        "-v", "/mnt/user-data/uploads:/uploads:ro",
        "-w", "/workspace/openstudio-mcp-server",
        "openstudio-mcp-dev",
        "uv", "run", "python", "-m", "openstudio_mcp_server.server"
      ]
    }
  }
}
```

**Note:** The `:ro` flag makes the mount read-only for security.

---

## Best Practices

### For Users

1. **Place files in workspace before starting**: If possible, copy OSM files to `C:\openstudio-mcp-server\sample_files\models\` before using Claude

2. **Use copy_file for uploaded files**: When Claude uploads a file, use `copy_file` to move it to the workspace first

3. **Use descriptive filenames**: Helps fuzzy matching work better

4. **Check error messages**: They often include helpful suggestions

### For Claude/AI Assistants

1. **Try direct load first**: Attempt `load_osm_model` with the path user provides

2. **If load fails, try copy_file**: Use `copy_file` to move the file to workspace, then load

3. **Use fuzzy matching for partial names**: When user says "load the office model", search with partial name

4. **Handle errors gracefully**: Parse error messages for suggestions and try alternatives

5. **Provide feedback**: Let user know when files are being copied or if access issues occur

---

## Troubleshooting

### Issue: "OSM file not found"

**Cause**: File not in any searched location

**Solutions**:
1. Use `copy_file` to copy from upload location to workspace
2. Check if file is in workspace: should be in `sample_files/models/`
3. Use fuzzy matching with partial filename
4. Add volume mount to Claude Desktop config

### Issue: "Permission denied"

**Cause**: Docker container doesn't have read permission

**Solutions**:
1. Check file permissions: `ls -l /path/to/file`
2. Use read-only mounts (`:ro`) in Docker config
3. Copy file to workspace where container has full access

### Issue: "Target file already exists"

**Cause**: Trying to copy to location with existing file

**Solution**: Use `overwrite=True` parameter:
```python
copy_file(source_path="model.osm", target_path="output.osm", overwrite=True)
```

### Issue: Fuzzy matching not working

**Cause**: File might be in a non-searched location

**Solutions**:
1. Check file is in workspace, sample_files, or outputs directory
2. Use more specific search terms
3. Use absolute path if you know it

---

## Technical Details

### Path Resolution Implementation

Located in: `openstudio_mcp_server/utils/path_utils.py`

Key functions:
- `resolve_path()` - Main resolution function with fuzzy matching
- `resolve_osm_path()` - Specialized for OSM files
- `resolve_idf_path()` - Specialized for IDF files
- `resolve_output_path()` - For creating new output files
- `PathResolver.suggest_similar_paths()` - Fuzzy matching implementation

### Integration Points

1. **openstudio_manager.py**:
   - `load_osm_file()` uses `resolve_osm_path()`
   - `save_osm_file()` uses `resolve_output_path()`
   - `convert_to_idf()` uses `resolve_output_path()`
   - `copy_file()` uses `resolve_path()` with fuzzy matching

2. **server.py**:
   - `copy_file` tool exposes the functionality to Claude
   - All file tools benefit from intelligent path resolution

---

## Example Workflow in Claude Desktop

**User**: "Load my office building model"

**Claude's Steps**:

1. **Try direct load**:
   ```python
   load_osm_model("office building")
   ```

2. **If fails, check error for upload path**:
   Error might say: "File not found: /mnt/user-data/uploads/office-building.osm"

3. **Copy to workspace**:
   ```python
   copy_file(
       source_path="/mnt/user-data/uploads/office-building.osm",
       target_path="office-building.osm"
   )
   ```

4. **Load from workspace**:
   ```python
   load_osm_model("office-building.osm")
   ```

5. **Report to user**:
   "I've loaded your office building model. It contains 24 spaces and 8 thermal zones."

---

## Summary

The OpenStudio MCP Server's file access system provides:

✅ **Intelligent path resolution** - Finds files in multiple locations
✅ **Fuzzy matching** - Handles partial names and typos
✅ **copy_file tool** - Moves uploaded files to accessible locations
✅ **Detailed error messages** - Helpful suggestions when files not found
✅ **Flexible configuration** - Additional mounts can be added

This makes the system much more robust when working with user-uploaded files in Claude Desktop.

---

## Further Reading

- [QUICK_START_UPDATED.md](QUICK_START_UPDATED.md) - Getting started guide
- [README.md](README.md) - Full documentation
- [TOOL_WRAPPER_EXAMPLES.md](TOOL_WRAPPER_EXAMPLES.md) - Adding new tools

For issues or questions, see: [GitHub Issues](https://github.com/roruizf/openstudio-mcp-server/issues)
