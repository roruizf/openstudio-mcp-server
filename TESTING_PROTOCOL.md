# OpenStudio MCP Server - Testing Protocol

**Version:** 1.0
**Last Updated:** 2025-01-09
**Purpose:** Standard Operating Procedure for verifying the OpenStudio MCP Server

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Testing Matrix](#testing-matrix)
   - [Workflow 1: Local Environment (Anaconda/WSL)](#workflow-1-local-environment-anacondawsl)
   - [Workflow 2: Docker Environment](#workflow-2-docker-environment)
3. [Troubleshooting Guide](#troubleshooting-guide)
4. [Validation Checklist](#validation-checklist)

---

## Prerequisites

### For Local Environment Testing

**Required Software:**
- **Anaconda/Miniconda** - Python environment manager
- **OpenStudio 3.7.0** - System installation (NOT pip package)
  - Download: https://github.com/NREL/OpenStudio/releases/tag/v3.7.0
  - Install to: `/usr/local/openstudio-3.7.0` (Linux)
- **uv** - Fast Python package installer
  ```bash
  pip install uv
  ```
- **Node.js 20+** - For MCP Inspector
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt-get install -y nodejs
  ```

**System Requirements:**
- Linux (WSL2 on Windows, or native Linux)
- 4GB+ RAM
- 2GB+ disk space

### For Docker Environment Testing

**Required Software:**
- **Visual Studio Code** - Code editor with Dev Containers support
- **Dev Containers Extension** - `ms-vscode-remote.remote-containers`
- **Docker Desktop** - Container runtime
  - Windows/Mac: Docker Desktop
  - Linux: Docker Engine + Docker Compose

**System Requirements:**
- 8GB+ RAM
- 10GB+ disk space
- Docker running and accessible

---

## Testing Matrix

## Workflow 1: Local Environment (Anaconda/WSL)

### Step 1: Environment Setup

**1.1 Create Conda Environment**
```bash
# Navigate to project root
cd /path/to/openstudio-mcp-server

# Create conda environment
conda create -n openstudio-mcp python=3.12 -y
conda activate openstudio-mcp
```

**1.2 Set Critical Environment Variables**

⚠️ **CRITICAL:** OpenStudio requires specific environment variables to find the system installation.

```bash
# Add to ~/.bashrc or run each session:
export OPENSTUDIO_VERSION=3.7.0
export OPENSTUDIO_PATH=/usr/local/openstudio-${OPENSTUDIO_VERSION}
export PYTHONPATH="${OPENSTUDIO_PATH}/Python:${PYTHONPATH}"
export LD_LIBRARY_PATH="${OPENSTUDIO_PATH}/lib:${LD_LIBRARY_PATH}"
export PATH="${OPENSTUDIO_PATH}/bin:${PATH}"
```

**Verify Variables:**
```bash
echo "OPENSTUDIO_PATH: $OPENSTUDIO_PATH"
echo "PYTHONPATH: $PYTHONPATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
```

**Expected Output:**
```
OPENSTUDIO_PATH: /usr/local/openstudio-3.7.0
PYTHONPATH: /usr/local/openstudio-3.7.0/Python:...
LD_LIBRARY_PATH: /usr/local/openstudio-3.7.0/lib:...
```

### Step 2: Install Dependencies

**2.1 Navigate to Nested Directory**
```bash
# IMPORTANT: The project uses nested structure
cd openstudio-mcp-server
```

**2.2 Install Project Dependencies**
```bash
# Install all dependencies including dev tools
uv sync --extra dev
```

**Expected Output:**
```
Resolved XX packages in XXXms
Installed XX packages in XXXms
```

### Step 3: Sanity Check - Verify OpenStudio Bindings

**3.1 Test OpenStudio Import**
```bash
python3 -c "import openstudio; print(f'OpenStudio Version: {openstudio.openStudioVersion()}')"
```

**Expected Output:**
```
OpenStudio Version: 3.7.0
```

**3.2 Test MCP Server Imports**
```bash
python3 -c "from openstudio_mcp_server.config import get_config; from openstudio_mcp_server.openstudio_tools import OpenStudioManager; print('✓ All imports successful')"
```

**Expected Output:**
```
✓ All imports successful
```

### Step 4: Start MCP Inspector

**4.1 Launch Inspector with Server**
```bash
# From openstudio-mcp-server/ directory (nested level)
npx @modelcontextprotocol/inspector uv run openstudio_mcp_server/server.py
```

**Expected Output:**
```
MCP Inspector running on http://localhost:6274
Proxy WebSocket listening on port 6277
Server started successfully
```

**4.2 Access Web Interface**
- Open browser to: `http://localhost:6274`
- Should see MCP Inspector UI
- Connection status should show: **Connected** (green)

### Step 5: Validation Tests

**5.1 Test Tool Discovery**
In MCP Inspector, click "List Tools". Should see:
- `load_osm_model` - Load OpenStudio models
- `get_model_summary` - Get model information
- `list_spaces` - List building spaces
- `list_thermal_zones` - List thermal zones
- And more...

**5.2 Test Model Loading**

**Call:** `load_osm_model`
**Arguments:**
```json
{
  "file_path": "sample_files/models/R2F-Office-Hub-006.osm",
  "translate_version": true
}
```

**Expected Response:**
```json
{
  "status": "success",
  "file_path": "/path/to/sample_files/models/R2F-Office-Hub-006.osm",
  "model_loaded": true,
  "translated": true
}
```

**5.3 Test Model Query**

**Call:** `get_model_summary`
**Arguments:** (none)

**Expected Response:**
```json
{
  "status": "success",
  "summary": {
    "spaces_count": X,
    "thermal_zones_count": Y,
    "surfaces_count": Z,
    ...
  }
}
```

### Step 6: Stop Server

Press `Ctrl+C` in terminal to stop the server gracefully.

---

## Workflow 2: Docker Environment

### Step 1: Container Build

**1.1 Open Project in VS Code**
```bash
code /path/to/openstudio-mcp-server
```

**1.2 Rebuild Dev Container**
- Press `F1` (or `Ctrl+Shift+P`)
- Type: "Dev Containers: Rebuild Container"
- Select and confirm

**Expected Output:**
```
Building container...
Installing dependencies with uv sync --extra dev...
Container ready!
```

**1.3 Verify Container Environment**
```bash
# Inside VS Code terminal:
pwd
```

**Expected Output:**
```
/workspace/openstudio-mcp-server
```

### Step 2: Port Forwarding Verification

**2.1 Check Forwarded Ports**
- In VS Code, open "PORTS" tab (bottom panel)
- Should see:
  - **6274** - MCP Inspector (should auto-open browser)
  - **6277** - MCP Inspector Proxy
  - 8080 - HTTP Server (Alternative)
  - 3000 - Development Server

**2.2 Manual Port Forward (if needed)**
If port 6277 is not listed:
- Click "Forward a Port"
- Enter: `6277`
- Label: "MCP Inspector Proxy"

### Step 3: Environment Verification

**3.1 Verify OpenStudio Installation**
```bash
python3 -c "import openstudio; print(openstudio.openStudioVersion())"
```

**Expected Output:**
```
3.7.0
```

**3.2 Verify Project Structure**
```bash
ls -l
```

**Expected Output:**
```
openstudio_mcp_server/
openstudio_toolkit/
tests/
sample_files/
pyproject.toml
...
```

### Step 4: Start MCP Inspector

**4.1 Launch from VS Code Terminal**
```bash
npx @modelcontextprotocol/inspector uv run openstudio_mcp_server/server.py
```

**4.2 Access Inspector**
- Browser should auto-open to `http://localhost:6274`
- Or manually navigate to `http://localhost:6274`

**Expected Behavior:**
- Web UI loads successfully
- "Connect" button becomes "Connected" (green)
- No connection errors in browser console

### Step 5: Run Same Validation Tests

Follow **Step 5** from [Workflow 1](#step-5-validation-tests) above.

### Step 6: Additional Docker Tests

**6.1 Test File Persistence**
```bash
# Create a test file
echo "test" > test_output.txt

# Rebuild container and verify file persists
ls test_output.txt
```

**6.2 Test Volume Mounts**
```bash
# Check workspace mount
df -h | grep workspace
```

**Expected Output:**
```
/workspace/openstudio-mcp-server
```

**6.3 Test Volume Access (Host C: Drive) - CRITICAL TEST**

This test verifies that the `-v C:\:/mnt/c` mount is working correctly, allowing the container to read/write files on your host machine.

**Prerequisites:**
- Create a test OSM file on your C: drive (e.g., in Downloads folder)
- Or use an existing OSM file

**Test Steps:**

**Step 1: Create Test File on Host (if needed)**
```bash
# On Windows host (PowerShell or CMD):
# Create a test file in Downloads
copy sample_files\models\*.osm C:\Users\<YourName>\Downloads\test_model.osm
```

**Step 2: Test Loading from `/mnt/c`**

In MCP Inspector, call `load_osm_model`:

**Arguments:**
```json
{
  "file_path": "/mnt/c/Users/<YourName>/Downloads/test_model.osm",
  "translate_version": true
}
```

**Expected Response:**
```json
{
  "status": "success",
  "file_path": "/mnt/c/Users/<YourName>/Downloads/test_model.osm",
  "model_loaded": true
}
```

**Step 3: Test Saving to `/mnt/c`**

Call `save_osm_model`:

**Arguments:**
```json
{
  "file_path": "/mnt/c/Users/<YourName>/Documents/test_model_saved.osm"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Successfully saved OSM file: test_model_saved.osm",
  "file_path": "/mnt/c/Users/<YourName>/Documents/test_model_saved.osm"
}
```

**Step 4: Verify File Exists on Host**
```bash
# On Windows host:
dir C:\Users\<YourName>\Documents\test_model_saved.osm
```

**Expected Result:**
File should exist and be a valid OSM file.

**Step 5: Test IDF Export to `/mnt/c`**

Call `convert_to_idf`:

**Arguments:**
```json
{
  "output_path": "/mnt/c/Users/<YourName>/Documents/test_model.idf"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Successfully converted to IDF: test_model.idf",
  "file_path": "/mnt/c/Users/<YourName>/Documents/test_model.idf"
}
```

**Step 6: Verify IDF on Host**
```bash
# On Windows host:
dir C:\Users\<YourName>\Documents\test_model.idf
```

**Success Criteria:**
- ✅ Model loads from `/mnt/c/Users/.../Downloads/`
- ✅ Model saves to `/mnt/c/Users/.../Documents/`
- ✅ IDF exports to `/mnt/c/Users/.../Documents/`
- ✅ All files persist on host machine after container stops
- ✅ No permission errors

**If This Test Fails:**
1. Check Docker Desktop → Settings → Resources → File Sharing
2. Ensure C: drive is listed and enabled
3. Restart Docker Desktop
4. Verify the `-v C:\:/mnt/c` mount in devcontainer.json or claude_desktop_config.json

---

## Troubleshooting Guide

### Common Errors and Solutions

#### Error 1: `ModuleNotFoundError: No module named 'openstudio'`

**Symptom:**
```
ModuleNotFoundError: No module named 'openstudio'
```

**Cause:** OpenStudio Python bindings not found in PYTHONPATH

**Solution (Local Environment):**
```bash
# 1. Verify OpenStudio installation exists
ls /usr/local/openstudio-3.7.0/Python

# 2. Set PYTHONPATH correctly
export PYTHONPATH="/usr/local/openstudio-3.7.0/Python:${PYTHONPATH}"

# 3. Verify fix
python3 -c "import openstudio; print(openstudio.openStudioVersion())"
```

**Solution (Docker):**
```bash
# Rebuild container - Dockerfile already sets PYTHONPATH
# In VS Code: F1 > "Dev Containers: Rebuild Container"
```

---

#### Error 2: `Invalid origin` or `Connection Refused` in MCP Inspector

**Symptom:**
- MCP Inspector shows "Error Connecting to MCP Inspector Proxy"
- Browser console shows: `WebSocket connection failed`

**Cause:** Port 6277 (WebSocket proxy) not forwarded or process conflict

**Solution 1 - Port Forwarding:**
```bash
# Check if port 6277 is forwarded
# In VS Code PORTS tab, add 6277 if missing
```

**Solution 2 - Kill Conflicting Processes:**
```bash
# Find process using port 6277
lsof -i :6277

# Kill the process
kill -9 <PID>

# Or kill all node processes
pkill -f inspector
```

**Solution 3 - Restart Inspector:**
```bash
# Stop: Ctrl+C
# Start:
npx @modelcontextprotocol/inspector uv run openstudio_mcp_server/server.py
```

---

#### Error 3: `SyntaxError: Unexpected token 'u', "[utilities"... is not valid JSON`

**Symptom:**
```
SyntaxError: Unexpected token 'u', "[utilities."... is not valid JSON
```

**Cause:** A tool is returning Python string representation instead of valid JSON

**Solution:**

**Step 1 - Identify the Problematic Tool:**
Check which tool call triggered the error in the Inspector logs.

**Step 2 - Verify Code Uses `json.dumps()`:**
```bash
# Search for the tool function in server.py
grep -A 20 "async def <tool_name>" openstudio_mcp_server/server.py
```

**Step 3 - Ensure Proper Serialization:**
All tool returns should use:
```python
return json.dumps(result, indent=2)
```

**NOT:**
```python
return str(result)  # ❌ WRONG - creates Python representation
return result       # ❌ WRONG - not serialized
```

**Step 4 - Rebuild Container:**
```bash
# After code fix, rebuild to apply changes
# VS Code: F1 > "Dev Containers: Rebuild Container"
```

---

#### Error 4: `No pyproject.toml found in current directory`

**Symptom:**
```
error: No `pyproject.toml` found in current directory
```

**Cause:** Running `uv sync` from wrong directory

**Solution:**
```bash
# Navigate to nested directory where pyproject.toml exists
cd openstudio-mcp-server

# Verify you're in the right place
ls pyproject.toml

# Now run uv sync
uv sync --extra dev
```

---

#### Error 5: `Failed to load OSM file: version translation failed`

**Symptom:**
```json
{
  "status": "error",
  "error": "Failed to load OSM file: version translation failed"
}
```

**Cause:** OSM file version incompatible with OpenStudio 3.7.0

**Solution:**
```bash
# Option 1: Load without version translation
# In load_osm_model call, set translate_version: false

# Option 2: Manually upgrade OSM file
openstudio_cli measure -r /path/to/model.osm
```

---

#### Error 6: Docker Build Fails - `dpkg: error processing openstudio`

**Symptom:**
```
dpkg: error processing package openstudio (--install)
```

**Cause:** Architecture mismatch or corrupted download

**Solution:**
```bash
# Check your architecture
uname -m

# If arm64/aarch64, verify Dockerfile uses ARM build:
# OpenStudio-3.7.0+d5269793f1-Ubuntu-20.04-arm64.deb

# If x86_64, verify uses x86_64 build:
# OpenStudio-3.7.0+d5269793f1-Ubuntu-20.04-x86_64.deb

# Rebuild container with clean cache
# VS Code: F1 > "Dev Containers: Rebuild Without Cache"
```

---

## Validation Checklist

Use this checklist to verify a complete test cycle:

### Pre-Test Setup
- [ ] Environment variables set (Local) or Container built (Docker)
- [ ] Dependencies installed (`uv sync --extra dev`)
- [ ] OpenStudio import successful (`import openstudio`)
- [ ] All ports forwarded (6274, 6277 for Docker)

### Server Startup
- [ ] MCP Inspector launches without errors
- [ ] Web UI accessible at `http://localhost:6274`
- [ ] Connection status shows "Connected" (green)
- [ ] No errors in browser console (F12)

### Tool Functionality
- [ ] Tool list loads (shows 15+ tools)
- [ ] `load_osm_model` works with sample file
- [ ] `get_model_summary` returns valid data
- [ ] `list_spaces` returns space list
- [ ] No JSON syntax errors in responses

### Error Handling
- [ ] Invalid file path shows proper error message
- [ ] Missing model shows "No model loaded" error
- [ ] All errors return valid JSON format

### Cleanup
- [ ] Server stops cleanly (Ctrl+C)
- [ ] No zombie processes remain
- [ ] Ports released (can restart immediately)

---

## How to Debug Docker Volumes

### Using MCP Inspector with Docker

When debugging Docker volume mounts (especially the critical `-v C:\:/mnt/c` mount), the **only reliable way** to verify file access is to run the MCP Inspector against the exact Docker configuration that Claude Desktop uses.

This ensures you're testing:
- ✅ Volume mounts work correctly
- ✅ Server can read files from `/mnt/c/Users/.../Downloads/`
- ✅ Server can write files to `/mnt/c/Users/.../Documents/`
- ✅ IDF exports persist on the host machine

### Manual Inspector Command (Mimics Claude Desktop)

**From Project Root Directory:**

**Windows (PowerShell):**
```powershell
npx @modelcontextprotocol/inspector docker run --rm -i `
  -v "C:\:/mnt/c" `
  -v "${PWD}:/workspace" `
  -w "/workspace/openstudio-mcp-server" `
  openstudio-mcp-dev `
  uv run openstudio_mcp_server/server.py
```

**Windows (CMD):**
```cmd
npx @modelcontextprotocol/inspector docker run --rm -i ^
  -v "C:\:/mnt/c" ^
  -v "%CD%:/workspace" ^
  -w "/workspace/openstudio-mcp-server" ^
  openstudio-mcp-dev ^
  uv run openstudio_mcp_server/server.py
```

**Linux/WSL:**
```bash
npx @modelcontextprotocol/inspector docker run --rm -i \
  -v "C:\:/mnt/c" \
  -v "$(pwd):/workspace" \
  -w "/workspace/openstudio-mcp-server" \
  openstudio-mcp-dev \
  uv run openstudio_mcp_server/server.py
```

### What This Command Does

1. **`npx @modelcontextprotocol/inspector`** - Launches MCP Inspector web UI
2. **`docker run --rm -i`** - Runs container interactively, removes when done
3. **`-v "C:\:/mnt/c"`** - Mounts C: drive to `/mnt/c` (FILE ACCESS mount)
4. **`-v "$(pwd):/workspace"`** - Mounts project source code (SERVER CODE mount)
5. **`-w "/workspace/openstudio-mcp-server"`** - Sets working directory to nested folder
6. **`openstudio-mcp-dev`** - Uses the pre-built Docker image
7. **`uv run openstudio_mcp_server/server.py`** - Starts the MCP server

### Critical Tests to Perform

Once Inspector is running (opens browser to `http://localhost:6274`):

#### Test 1: Load Model from Host Machine
```json
{
  "tool": "load_osm_model",
  "arguments": {
    "file_path": "/mnt/c/Users/<YourName>/Downloads/test_model.osm",
    "translate_version": true
  }
}
```

**Success:** Model loads from your Downloads folder
**Failure:** `FileNotFoundError` → Volume mount not working

#### Test 2: Save Model to Host Machine
```json
{
  "tool": "save_osm_model",
  "arguments": {
    "file_path": "/mnt/c/Users/<YourName>/Documents/test_saved.osm"
  }
}
```

**Success:** File appears in your Documents folder
**Failure:** File doesn't persist → Volume mount read-only or broken

#### Test 3: Export IDF to Host Machine
```json
{
  "tool": "convert_to_idf",
  "arguments": {
    "output_path": "/mnt/c/Users/<YourName>/Documents/test_export.idf"
  }
}
```

**Success:** IDF file appears in Documents
**Failure:** File doesn't persist → Volume mount issue

### Why This Is the Only Reliable Test

Running the server **without** Docker (e.g., locally with `uv run`) will NOT catch volume mount issues because:
- ❌ No `/mnt/c` path exists outside Docker
- ❌ Cannot verify Claude Desktop's exact runtime environment
- ❌ File access behavior differs from containerized environment

**This manual Docker Inspector test is the ONLY way to verify that `save_osm_model` and `convert_to_idf` can actually write to the host disk before deploying to Claude Desktop.**

### Troubleshooting Docker Volume Issues

If files don't persist after tests:

1. **Check Docker Desktop File Sharing:**
   - Open Docker Desktop → Settings → Resources → File Sharing
   - Ensure C: drive is listed and enabled
   - Click "Apply & Restart"

2. **Verify Volume Mount in Running Container:**
   ```bash
   docker run --rm -it -v "C:\:/mnt/c" alpine ls -la /mnt/c/Users
   ```
   Should list user directories. If empty or error → Docker Desktop file sharing issue.

3. **Check Windows Path Length:**
   - Windows has 260-char limit
   - Use short paths like `C:\openstudio-mcp-server`
   - Avoid deep nested directories

4. **Restart Docker Desktop:**
   - Sometimes mounts require Docker Desktop restart to take effect

---

## Notes for Maintainers

**Key Differences from EnergyPlus MCP:**
- OpenStudio uses **system .deb installation**, not pip package
- Requires **LD_LIBRARY_PATH** for shared libraries
- Uses **nested project structure** (openstudio-mcp-server/openstudio-mcp-server/)
- Additional package: `openstudio_toolkit` for utilities

**Testing Frequency:**
- **Every code change:** Run Workflow 1 or 2
- **Before commits:** Complete validation checklist
- **After dependency updates:** Full test cycle + rebuild
- **Before releases:** Both workflows + all validation tests

**Continuous Integration:**
- Consider adding GitHub Actions workflow
- Test both local and Docker environments
- Validate against multiple OSM file versions
- Check for JSON serialization issues

---

**End of Testing Protocol**
