# Claude Desktop Setup for OpenStudio MCP Server

**Purpose:** Configure Claude Desktop to use the OpenStudio MCP Server running in Docker

**Platform:** Windows (with Docker Desktop)

---

## Golden Configuration

Add this configuration to your Claude Desktop `claude_desktop_config.json`:

**File Location:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Configuration JSON

```json
{
  "mcpServers": {
    "openstudio": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v", "C:\\:/mnt/c",
        "-v", "C:\\PATH\\TO\\YOUR\\openstudio-mcp-server:/workspace",
        "-w", "/workspace/openstudio-mcp-server",
        "openstudio-mcp-dev",
        "uv", "run", "openstudio_mcp_server/server.py"
      ]
    }
  }
}
```

> **💡 Windows Setup Tip (Best Practice):**
>
> We strongly recommend cloning this repository to a **short root path** like `C:\openstudio-mcp-server` instead of deep user directories like `C:\Users\YourName\Documents\GitHub\openstudio-mcp-server`.
>
> **Why?** Windows has a 260-character path limit that can cause issues with nested project directories and long dependency paths. This recommendation follows EnergyPlus best practices for avoiding path-related build and runtime errors.
>
> **Example:**
> - ✅ **Recommended:** `C:\openstudio-mcp-server`
> - ⚠️ **Avoid:** `C:\Users\YourName\Documents\Projects\BuildingEnergy\openstudio-mcp-server`

---

## Critical Configuration Elements

### Understanding the Two Volume Mounts

The Docker configuration requires **two separate volume mounts**, each serving a distinct purpose:

### 1. Volume Mount: C: Drive Access (User Files)

```json
"-v", "C:\\:/mnt/c"
```

**Purpose:** Grants the server **Read/Write access to your entire C: drive**, enabling it to load models from and save outputs to your host machine.

**Why This Is Critical:**
- Allows the MCP server to read/write files **directly to your hard drive**
- Users can access files in `Downloads`, `Documents`, `Desktop`, etc.
- Outputs persist on the host machine (not lost when container stops)

**Examples:**
```
Host Path:                        Container Path:
C:\Users\Name\Downloads\model.osm → /mnt/c/Users/Name/Downloads/model.osm
C:\Users\Name\Documents\output.idf → /mnt/c/Users/Name/Documents/output.idf
C:\Projects\buildings\            → /mnt/c/Projects/buildings/
```

### 2. Volume Mount: Server Source Code (Repository)

```json
"-v", "C:\\PATH\\TO\\YOUR\\openstudio-mcp-server:/workspace"
```

**Purpose:** Mounts the server's **source code** (the cloned repository) into the container at `/workspace`, enabling the container to execute the Python server.

**Important:** Replace `C:\\PATH\\TO\\YOUR\\openstudio-mcp-server` with the actual path where you cloned this repository.

**Example:**
- If you cloned to `C:\openstudio-mcp-server`, use: `"-v", "C:\\openstudio-mcp-server:/workspace"`
- If you cloned to `D:\Projects\openstudio-mcp-server`, use: `"-v", "D:\\Projects\\openstudio-mcp-server:/workspace"`

### 3. Working Directory

```json
"-w", "/workspace/openstudio-mcp-server"
```

**Purpose:** Sets the working directory inside the container to the nested project folder where `pyproject.toml` exists.

### 4. Container Image

```json
"openstudio-mcp-dev"
```

**Purpose:** The Docker image built from `.devcontainer/Dockerfile`.

**How to Build:**
```bash
# From repository root
docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev .devcontainer
```

---

## Usage Instructions

### Step 1: Build the Docker Image

**Option A: Using VS Code Dev Container (Recommended)**
1. Open repository in VS Code
2. Press `F1` → "Dev Containers: Rebuild Container"
3. Wait for build to complete
4. The image `openstudio-mcp-dev` is created automatically

**Option B: Manual Docker Build**
```bash
cd C:\PATH\TO\YOUR\openstudio-mcp-server
docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev .devcontainer
```

**Verify Image Exists:**
```bash
docker images | grep openstudio-mcp-dev
```

Expected output:
```
openstudio-mcp-dev   latest   abc123def456   X minutes ago   X.XXG
```

### Step 2: Configure Claude Desktop

1. **Locate Config File:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - If file doesn't exist, create it

2. **Add Golden Configuration:**
   - Copy the JSON from above
   - **IMPORTANT:** Replace `C:\\PATH\\TO\\YOUR\\openstudio-mcp-server` with your actual repository path

3. **Save File**

### Step 3: Restart Claude Desktop

1. **Quit Claude Desktop** completely (check system tray)
2. **Reopen Claude Desktop**
3. **Verify Connection:**
   - Look for the hammer icon (🔨) in the chat interface
   - Click it to see available MCP tools
   - Should see: `load_osm_model`, `save_osm_model`, `convert_to_idf`, etc.

---

## File Access Pattern

### ⚠️ CRITICAL: How to Reference Files

**Users MUST use container paths (not host paths) when interacting with the MCP server:**

#### ❌ WRONG (Host Path)
```
C:\Users\Name\Downloads\model.osm
```

#### ✅ CORRECT (Container Path)
```
/mnt/c/Users/Name/Downloads/model.osm
```

### Example Conversation with Claude

**User:**
> Load this model: /mnt/c/Users/JohnDoe/Downloads/Office-Building.osm

**Claude (using MCP tool):**
```json
{
  "tool": "load_osm_model",
  "arguments": {
    "file_path": "/mnt/c/Users/JohnDoe/Downloads/Office-Building.osm"
  }
}
```

**User:**
> Convert it to IDF and save to my Documents folder

**Claude (using MCP tool):**
```json
{
  "tool": "convert_to_idf",
  "arguments": {
    "output_path": "/mnt/c/Users/JohnDoe/Documents/Office-Building.idf"
  }
}
```

---

## Common Path Mappings

| User's Typical Location | Container Path |
|-------------------------|----------------|
| Downloads folder | `/mnt/c/Users/<Username>/Downloads/` |
| Documents folder | `/mnt/c/Users/<Username>/Documents/` |
| Desktop | `/mnt/c/Users/<Username>/Desktop/` |
| C:\Projects | `/mnt/c/Projects/` |
| Sample files (project) | `/workspace/openstudio-mcp-server/sample_files/` |

---

## Troubleshooting

### Issue: "Container not found"

**Error:**
```
Error: No such container: openstudio-mcp-dev
```

**Solution:**
Build the Docker image (see Step 1 above)

### Issue: "Permission denied" when accessing files

**Error:**
```
PermissionError: [Errno 13] Permission denied: '/mnt/c/...'
```

**Solution:**
1. Check Docker Desktop settings → Resources → File Sharing
2. Ensure C: drive is shared
3. Restart Docker Desktop

### Issue: "File not found" even though it exists on C:

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/mnt/c/Users/Name/file.osm'
```

**Common Causes:**
1. **Wrong path format** - Use `/mnt/c/` not `C:\`
2. **Spaces in path** - Ensure path is quoted correctly
3. **Docker volume mount missing** - Verify `-v C:\\:/mnt/c` in config

**Solution:**
```bash
# Test if volume mount works
docker run --rm -v C:\:/mnt/c alpine ls /mnt/c/Users
```

Should list user directories. If error, check Docker Desktop file sharing settings.

### Issue: "Server won't start" or "Connection refused"

**Check Logs:**
```bash
# Run container manually to see errors
docker run --rm -it \
  -v C:\:/mnt/c \
  -v C:\PATH\TO\YOUR\openstudio-mcp-server:/workspace \
  -w /workspace/openstudio-mcp-server \
  openstudio-mcp-dev \
  uv run openstudio_mcp_server/server.py
```

Look for error messages in output.

### Issue: Output files disappear after container stops

**Cause:** Saving files inside container (not to `/mnt/c`)

**Solution:**
Always save outputs to `/mnt/c/...` paths, which persist on your host machine.

**Example:**
```
✅ GOOD: /mnt/c/Users/Name/Documents/output.idf
❌ BAD:  /tmp/output.idf (lost when container stops)
❌ BAD:  /workspace/output.idf (only in container volume)
```

---

## Advanced Configuration

### Using a Different Drive (D:, E:, etc.)

```json
"-v", "D:\\:/mnt/d",
"-v", "E:\\:/mnt/e"
```

Then reference files as `/mnt/d/...` or `/mnt/e/...`

### Limiting Volume Access (More Secure)

Instead of mounting entire C: drive:

```json
"-v", "C:\\Users\\YourName\\OpenStudioModels:/models",
```

Then files are accessible at `/models/...` only.

### Adding Environment Variables

```json
"args": [
  "run",
  "--rm",
  "-i",
  "-e", "LOG_LEVEL=DEBUG",
  "-v", "C:\\:/mnt/c",
  ...
]
```

---

## Security Considerations

**WARNING:** The configuration `-v C:\\:/mnt/c` gives the container READ/WRITE access to your entire C: drive.

**Recommendations:**
1. Only use trusted Docker images
2. Review Dockerfile before building
3. Consider limiting mount to specific folders (see Advanced Configuration)
4. Do not share this configuration with untrusted users

---

## Updating the Server

When the OpenStudio MCP Server code is updated:

1. **Rebuild Docker Image:**
   ```bash
   docker build -f .devcontainer/Dockerfile -t openstudio-mcp-dev .devcontainer
   ```

2. **Restart Claude Desktop**
   - Changes take effect immediately after restart

---

## Additional Resources

- **Project README:** `/openstudio-mcp-server/README.md`
- **Testing Protocol:** `/openstudio-mcp-server/TESTING_PROTOCOL.md`
- **Docker Documentation:** https://docs.docker.com/
- **MCP Protocol:** https://modelcontextprotocol.io/

---

**End of Claude Desktop Setup Guide**
