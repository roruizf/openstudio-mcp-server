# Claude AI Developer Guide - OpenStudio MCP Server

**Purpose:** Guide AI assistants working with this Docker-based MCP server for OpenStudio building energy modeling.

**Critical Context:** This server runs inside Docker to manage complex system-level OpenStudio dependencies (Python bindings, Ruby libraries, X11 libraries).

---

## Commands Reference

### Docker Build

Build the Docker image after changing dependencies or Dockerfile:

```bash
docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev .
```

**When to rebuild:**
- After modifying `pyproject.toml` dependencies
- After changing `.devcontainer/Dockerfile`
- After updating OpenStudio version

### Docker Run (Production)

Run the server in Docker as configured in Claude Desktop:

```bash
docker run --rm -i \
  -v C:\:/mnt/c \
  -v C:\openstudio-mcp-server:/workspace \
  -w /workspace/openstudio-mcp-server \
  openstudio-mcp-dev \
  uv run openstudio_mcp_server/server.py
```

**Volume Mounts:**
- `-v C:\:/mnt/c` - Entire C: drive access (enables smart path translation)
- `-v C:\openstudio-mcp-server:/workspace` - Server source code

### Local Debug (Inside Container)

For testing without Claude Desktop connection:

```bash
uv run openstudio_mcp_server/server.py
```

**Requirements:**
- Must run inside the Docker container (or with OpenStudio installed locally)
- Container must have access to OpenStudio Python bindings via `PYTHONPATH`

---

## Architecture & Components

### Overview

```
┌─────────────────────────────────────────────────────┐
│ Claude Desktop (Client)                             │
└────────────────┬────────────────────────────────────┘
                 │ MCP Protocol (stdio)
                 ↓
┌─────────────────────────────────────────────────────┐
│ Docker Container (openstudio-mcp-dev)               │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ server.py (FastMCP Entry Point)              │  │
│  │  - Defines MCP tools                         │  │
│  │  - Handles client communication              │  │
│  │  - Routes requests to OpenStudioManager      │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                │
│  ┌─────────────────▼────────────────────────────┐  │
│  │ openstudio_tools.py (Controller Layer)       │  │
│  │  - OpenStudioManager class                   │  │
│  │  - Minimal logic (validation, path resolution) │
│  │  - Calls openstudio_toolkit functions        │  │
│  │  - Formats responses as JSON                 │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                │
│  ┌─────────────────▼────────────────────────────┐  │
│  │ openstudio_toolkit/ (Business Logic)         │  │
│  │  - Robust OpenStudio operations              │  │
│  │  - Direct interaction with OpenStudio API    │  │
│  │  - Pure functions (no state)                 │  │
│  │  - osm_objects/, tasks/, utils/              │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  System Dependencies:                               │
│  - OpenStudio 3.7.0 (installed in /usr/local/)     │
│  - Python 3.12                                      │
│  - X11 libraries (for OpenStudio rendering)        │
└─────────────────────────────────────────────────────┘
```

### Component Details

#### 1. **server.py** (FastMCP Entry Point)

**Location:** `openstudio_mcp_server/server.py`

**Responsibilities:**
- Initializes FastMCP server
- Defines all MCP tools using `@mcp.tool()` decorator
- Handles MCP protocol communication (stdio)
- Routes tool calls to `OpenStudioManager`

**Example:**
```python
@mcp.tool()
async def load_osm_model(file_path: str, translate_version: bool = True) -> str:
    """Load an OpenStudio Model (OSM) file."""
    result = os_manager.load_osm_file(file_path, translate_version)
    return ensure_json_response(result)
```

**Key Point:** This layer should contain NO business logic - only tool definitions and routing.

---

#### 2. **openstudio_tools.py** (Controller/Bridge Layer)

**Location:** `openstudio_mcp_server/openstudio_tools.py`

**Responsibilities:**
- `OpenStudioManager` class maintains state (current loaded model)
- Input validation and path resolution
- Calls `openstudio_toolkit` functions
- Formats responses as dictionaries (converted to JSON by server.py)

**Design Principle:** **MINIMAL LOGIC**

This layer acts as a **thin controller** that:
1. Receives inputs from Claude (via server.py)
2. Validates inputs (e.g., "is a model loaded?")
3. Resolves file paths (using `path_utils.py`)
4. Calls robust functions from `openstudio_toolkit`
5. Returns simple structured responses

**Example:**
```python
def load_osm_file(self, file_path: str, translate_version: bool = True) -> Dict[str, Any]:
    # 1. Resolve path (with smart Windows→Docker translation)
    resolved_path = resolve_osm_path(self.config, file_path)

    # 2. Call toolkit function (where the real logic lives)
    from openstudio_toolkit.utils.osm_utils import load_osm_file_as_model
    model = load_osm_file_as_model(resolved_path, translate_version)

    # 3. Update state
    self.current_model = model
    self.current_file_path = resolved_path

    # 4. Return formatted response
    return {"status": "success", "model_path": resolved_path, ...}
```

**What NOT to put here:**
- Complex OpenStudio API interactions → Put in `openstudio_toolkit`
- Data transformations or calculations → Put in `openstudio_toolkit`
- HVAC system logic, load calculations, etc. → Put in `openstudio_toolkit`

---

#### 3. **openstudio_toolkit/** (Business Logic Library)

**Location:** `openstudio_mcp_server/../openstudio_toolkit/`

**Responsibilities:**
- All robust OpenStudio operations
- Direct interaction with OpenStudio Python API
- Pure functions (no state management)
- Reusable across different interfaces (MCP, CLI, notebooks)

**Structure:**
```
openstudio_toolkit/
├── osm_objects/          # Object extraction (spaces, zones, HVAC, materials)
│   ├── spaces.py
│   ├── thermal_zones.py
│   ├── hvac_air_loops.py
│   └── ...
├── tasks/                # High-level workflows
│   ├── model_setup/
│   ├── model_qa_qc/
│   ├── simulation_setup/
│   └── results_analysis/
└── utils/                # Core utilities
    ├── osm_utils.py      # Load/save OSM, convert to IDF
    ├── eplus_utils.py    # EnergyPlus operations
    └── excel_utils.py    # Export to Excel
```

**Design Principle:** This is where the **real work happens**.

**Example:**
```python
# openstudio_toolkit/utils/osm_utils.py
def load_osm_file_as_model(osm_path: str, translate_version: bool = True):
    """Load OSM file and return OpenStudio Model object."""
    translator = openstudio.osversion.VersionTranslator()
    model = translator.loadModel(osm_path)
    if not model.is_initialized():
        raise ValueError(f"Failed to load model: {osm_path}")
    return model.get()
```

**Dependency Note:**
- Currently a **local package** within this repository
- Packaged alongside `openstudio_mcp_server` (see `pyproject.toml`)
- Designed as a separate module for potential future extraction to standalone library

---

## Folder Structure

```
openstudio-mcp-server/                    # Repository root
├── .devcontainer/
│   └── Dockerfile                        # Docker image definition (CRITICAL)
├── openstudio-mcp-server/                # Nested project directory
│   ├── openstudio_mcp_server/            # MCP server code
│   │   ├── server.py                     # FastMCP entry point
│   │   ├── openstudio_tools.py           # OpenStudioManager (controller)
│   │   ├── config.py                     # Configuration management
│   │   └── utils/
│   │       ├── path_utils.py             # Smart path resolution
│   │       └── json_utils.py             # JSON response formatting
│   ├── openstudio_toolkit/               # Business logic library
│   │   ├── osm_objects/                  # Object extraction modules
│   │   ├── tasks/                        # Workflow tasks
│   │   └── utils/                        # Core utilities (osm_utils, etc.)
│   ├── sample_files/                     # Sample models and weather files
│   │   ├── models/                       # .osm files
│   │   └── weather/                      # .epw files
│   ├── outputs/                          # Generated files (IDF, Excel, etc.)
│   ├── logs/                             # Server logs
│   ├── tests/                            # Test suite
│   └── pyproject.toml                    # Python dependencies
├── README.md                             # Main documentation
├── USER_GUIDE.md                         # End-user instructions
├── CLAUDE_DESKTOP_SETUP.md               # Docker configuration guide
└── DEVELOPER_NOTES.md                    # Technical implementation details
```

**Key Points:**
- **Docker context root:** `openstudio-mcp-server/` (for `.devcontainer/Dockerfile`)
- **Working directory in container:** `/workspace/openstudio-mcp-server` (the nested directory)
- **Volume mount:** Maps host `C:\openstudio-mcp-server` to container `/workspace`

---

## Development Workflow

### 1. Modifying Python Code

**For changes in `openstudio_mcp_server/` or `openstudio_toolkit/`:**
- Edit files directly
- Changes are live (volume-mounted from host)
- Restart Claude Desktop to reload the server

**No rebuild needed** - code changes are immediately reflected.

### 2. Modifying Dependencies

**If you change `pyproject.toml`:**

```bash
# MUST rebuild the Docker image
docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev .

# Then restart Claude Desktop to use the new image
```

**Why?** Dependencies are installed during Docker build via `uv`.

### 3. Modifying Dockerfile

**If you change `.devcontainer/Dockerfile`:**

```bash
# MUST rebuild with --no-cache to force fresh install
docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev . --no-cache

# Restart Claude Desktop
```

**Common reasons:**
- Updating OpenStudio version
- Adding system packages (apt-get)
- Changing environment variables

### 4. Testing Changes

**Option A: Test with Claude Desktop**
1. Restart Claude Desktop
2. Test tools in conversation

**Option B: Test with MCP Inspector**
```bash
# Inside the container
npx @modelcontextprotocol/inspector uv run openstudio_mcp_server/server.py
```

**Option C: Unit Tests**
```bash
# Inside the container
uv run pytest tests/
```

---

## Critical Dependencies

### System-Level (Installed in Docker)

**OpenStudio 3.7.0:**
- Installation: `/usr/local/openstudio-3.7.0`
- Python bindings: Available via `PYTHONPATH`
- Required for all model operations

**Why Docker?** OpenStudio has complex dependencies:
- Ruby libraries (`RUBYLIB`)
- X11 libraries (for rendering)
- Specific Python bindings
- Platform-specific binaries

### Python Dependencies (pyproject.toml)

**MCP Framework:**
- `mcp[cli]>=0.1.0` - Model Context Protocol

**Data & Visualization:**
- `pandas>=2.0.0` - Data manipulation
- `matplotlib>=3.7.0` - Plotting
- `plotly>=5.14.0` - Interactive plots
- `networkx>=3.0` - Graph analysis
- `openpyxl>=3.1.0` - Excel export

**Development:**
- `uv` - Fast Python package installer
- `pytest` - Testing framework

---

## Smart Path Translation

**Feature:** Automatically converts Windows paths to Docker paths.

**Location:** `openstudio_mcp_server/utils/path_utils.py`

**How it works:**
```python
# User provides Windows path:
"C:\\Users\\John\\Documents\\model.osm"

# Automatically translated to:
"/mnt/c/Users/John/Documents/model.osm"
```

**Requirements:**
- Docker mount: `-v C:\:/mnt/c` (enables C: drive access)
- Only works for C: drive (extendable to D:, E:, etc.)

**Benefits:**
- Users can copy-paste paths from Windows Explorer
- No manual path translation required
- Seamless UX across host and container

---

## Common Development Tasks

### Add a New MCP Tool

1. **Define in `server.py`:**
```python
@mcp.tool()
async def my_new_tool(param: str) -> str:
    """Tool description."""
    result = os_manager.my_new_method(param)
    return ensure_json_response(result)
```

2. **Implement in `openstudio_tools.py`:**
```python
def my_new_method(self, param: str) -> Dict[str, Any]:
    # Minimal logic here
    from openstudio_toolkit.my_module import do_work
    result = do_work(self.current_model, param)
    return {"status": "success", "result": result}
```

3. **Add business logic to `openstudio_toolkit/`:**
```python
def do_work(model, param):
    # Real OpenStudio operations here
    pass
```

### Add a New Dependency

1. Edit `pyproject.toml`:
```toml
dependencies = [
    "new-package>=1.0.0",
]
```

2. **MUST rebuild Docker image:**
```bash
docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev .
```

3. Restart Claude Desktop

### Update OpenStudio Version

1. Edit `.devcontainer/Dockerfile`:
```dockerfile
ARG OPENSTUDIO_VERSION=3.8.0
ARG OPENSTUDIO_SHA=<new-sha>
```

2. Rebuild with --no-cache:
```bash
docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev . --no-cache
```

---

## Troubleshooting

### "Module 'openstudio' not found"

**Cause:** Python can't find OpenStudio bindings

**Solution:**
- Ensure running inside Docker container
- Check `PYTHONPATH` includes `/usr/local/openstudio-3.7.0/Python`
- Verify OpenStudio installed: `ls /usr/local/openstudio-3.7.0`

### "File not found" errors

**Cause:** Path resolution issue

**Solution:**
- Check smart path translation in `path_utils.py`
- Verify Docker mount: `-v C:\:/mnt/c`
- Use absolute Windows paths (e.g., `C:\Users\...`)

### Changes not reflected

**For code changes:**
- Just restart Claude Desktop (no rebuild needed)

**For dependency changes:**
- MUST rebuild Docker image
- Then restart Claude Desktop

### Container permission errors

**Cause:** Files owned by root, user is `vscode`

**Solution:**
- Container runs as `vscode` user (non-root)
- Ensure workspace has correct permissions
- Check volume mount ownership

---

## Best Practices

### 1. Layer Separation

**server.py:**
- Only tool definitions
- No business logic

**openstudio_tools.py:**
- Thin controller
- Validation & path resolution
- State management (current model)
- Calls to toolkit

**openstudio_toolkit/:**
- All business logic
- Pure functions
- Testable in isolation

### 2. Error Handling

**Always return JSON with status:**
```python
{
    "status": "success" | "error",
    "message": "Human-readable message",
    "data": {...}  # Optional
}
```

**Use try-except in controller:**
```python
try:
    result = toolkit_function()
    return {"status": "success", "data": result}
except Exception as e:
    logger.error(f"Error: {e}")
    return {"status": "error", "message": str(e)}
```

### 3. Logging

**Use structured logging:**
```python
logger.info(f"Loading model: {file_path}")
logger.debug(f"Model has {num_spaces} spaces")
logger.error(f"Failed to load: {e}")
```

**Log levels:**
- `DEBUG` - Detailed info for debugging
- `INFO` - Normal operations
- `WARNING` - Potential issues
- `ERROR` - Actual errors

### 4. Testing

**Unit tests for toolkit:**
```python
# tests/test_osm_utils.py
def test_load_osm_file():
    model = load_osm_file_as_model("sample.osm")
    assert model is not None
```

**Integration tests for manager:**
```python
# tests/test_openstudio_manager.py
def test_manager_load_file(manager):
    result = manager.load_osm_file("sample.osm")
    assert result["status"] == "success"
```

---

## Resources

- **[README.md](README.md)** - Main documentation
- **[USER_GUIDE.md](USER_GUIDE.md)** - End-user guide (smart path handling)
- **[CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md)** - Docker configuration details
- **[DEVELOPER_NOTES.md](DEVELOPER_NOTES.md)** - Technical implementation details
- **[OpenStudio SDK Documentation](https://openstudio-sdk-documentation.s3.amazonaws.com/index.html)** - OpenStudio API reference

---

## Summary

**Key Takeaways for AI Assistants:**

1. **Docker-First:** Always rebuild image after dependency changes
2. **Layer Separation:** Keep `openstudio_tools.py` thin - business logic goes in `openstudio_toolkit`
3. **Smart Paths:** Windows paths auto-translate (requires `-v C:\:/mnt/c` mount)
4. **State Management:** `OpenStudioManager` holds current model state
5. **JSON Responses:** Always return structured JSON with status field
6. **Testing:** Test toolkit functions in isolation, then integration with manager
7. **Dependencies:** OpenStudio bindings from system installation, not pip package

**When in doubt:**
- Check if running inside Docker
- Verify volume mounts are correct
- Rebuild image if dependencies changed
- Review logs in `logs/openstudio_mcp_server.log`
