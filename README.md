# OpenStudio MCP Server

A **Model Context Protocol (MCP)** server that enables AI assistants like Claude to interact with **OpenStudio** building energy models. Load, inspect, and manipulate OpenStudio Model (OSM) files through a comprehensive set of tools accessible via natural language.

## Credits and Acknowledgments

This project is heavily based on the [**EnergyPlus MCP Server**](https://github.com/LBNL-ETA/energyplus-mcp) developed by **LBNL-ETA** (Lawrence Berkeley National Laboratory - Energy Technologies Area). The server architecture, tool structure, and implementation patterns have been replicated as closely as possible from their excellent work.

The tools in this server are built using the [**OpenStudio-Toolkit**](https://github.com/roruizf/OpenStudio-Toolkit) library, which provides Python interfaces to OpenStudio's building modeling capabilities.

This project was developed with the invaluable assistance of **Claude Code** powered by **Anthropic's Claude Sonnet 4.5**.

---

## Features

### Available Tools (20+)

#### 📁 **File & Model Management**
- `load_osm_model` - Load OpenStudio Model files with intelligent path resolution
- `save_osm_model` - Save modified models
- `convert_to_idf` - Export to EnergyPlus IDF format
- `copy_file` - Copy files with fuzzy matching and smart discovery
- `get_model_summary` - Get comprehensive model statistics
- `get_building_info` - Get building object details

#### 📊 **Visualization & Analysis**
- `apply_view_model` - Generate interactive HTML visualization (geometry, HVAC, zones, materials)
- `apply_space_type_and_construction_set_wizard` - Apply ASHRAE 90.1 building templates

#### 🏗️ **Building Geometry**
- `list_spaces` - List all spaces with properties
- `get_space_details` - Get detailed information about a specific space
- `list_thermal_zones` - List all thermal zones
- `get_thermal_zone_details` - Get detailed zone information

#### 🧱 **Materials & Constructions**
- `list_materials` - List all materials with thermal properties

#### 🌀 **HVAC Systems**
- `list_air_loops` - List all air loop HVAC systems

#### 💡 **Internal Loads**
- `list_people_loads` - List occupancy loads
- `list_lighting_loads` - List lighting power densities
- `list_electric_equipment` - List equipment loads

#### 📅 **Schedules**
- `list_schedule_rulesets` - List all schedule rulesets

#### ⚙️ **Server Management**
- `get_server_info` - Get server configuration and status
- `get_current_model_status` - Check currently loaded model

### Key Capabilities

- **Intelligent File Discovery**: Automatically finds files in multiple locations including Claude Desktop uploads
- **Fuzzy Matching**: Finds files even with partial names or typos
- **Dual Environment Support**: Works seamlessly in both Docker and Claude Desktop
- **Comprehensive API**: Covers building geometry, HVAC, loads, materials, and schedules

---

## Installation

### Prerequisites

- **Docker Desktop** (REQUIRED - recommended installation method)
- **Claude Desktop**, **VS Code**, or **Cursor** (for AI assistant integration)
- **Windows/Mac/Linux** system

### Quick Start (Docker - Recommended)

#### 1. Clone the Repository

```bash
git clone https://github.com/roruizf/openstudio-mcp-server.git
cd openstudio-mcp-server
```

#### 2. Build Docker Image

```bash
docker build -t openstudio-mcp-dev -f .devcontainer/Dockerfile .devcontainer
```

This builds a container with:
- Python 3.12
- **OpenStudio 3.7.0** (system installation with SDK and Python bindings)
- All required dependencies
- OpenStudio-Toolkit library

**Verify Build:**
```bash
docker images | grep openstudio-mcp-dev
```

#### 3. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Add this configuration (Windows example):**

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

**CRITICAL:** The configuration requires **two volume mounts** (see explanations below):
- **`-v C:\\:/mnt/c`** - Grants access to your C: drive for reading/writing model files
- **`-v C:\\PATH\\TO\\YOUR\\openstudio-mcp-server:/workspace`** - Mounts the server source code

**Important**: Replace `C:\\PATH\\TO\\YOUR\\openstudio-mcp-server` with your actual repository path.

> **📁 Outputs Directory:**
>
> Generated files (HTML visualizations, IDF exports, reports) are automatically saved to `openstudio-mcp-server/outputs/` inside the container, which maps to `C:\openstudio-mcp-server\outputs\` on your host machine through the workspace volume mount. The server creates this directory automatically with proper permissions.

📖 **For detailed setup instructions, see [CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md)**

#### 4. Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

#### 5. Verify Installation

In Claude Desktop, ask:
```
"What OpenStudio tools are available?"
```

Claude should list all available tools.

---

## File Access (CRITICAL)

### Understanding Docker Volume Mounts

The OpenStudio MCP Server runs inside a Docker container, which has its own isolated filesystem. To access files on your **host machine** (your computer), you must use **mounted paths**.

The configuration requires **two separate volume mounts**, each serving a distinct purpose:

### 1. C: Drive Access Mount: `-v C:\:/mnt/c`

**Purpose:** Grants the server **Read/Write access to your entire C: drive**, enabling it to load models from and save outputs to your host machine.

**This means:**
- Files on your C: drive are accessible at `/mnt/c/...` paths
- Outputs saved to `/mnt/c/...` persist on your host machine
- Without this mount, the container cannot access your files

### 2. Server Source Code Mount: `-v C:\PATH\TO\YOUR\openstudio-mcp-server:/workspace`

**Purpose:** Mounts the server's **source code** (the cloned repository) into the container at `/workspace`, enabling the container to execute the Python server.

**This means:**
- The server can access its own code, dependencies, and sample files
- Changes to server code on your host are reflected in the container
- Replace the placeholder path with where you actually cloned the repository

### How to Reference Files

#### ❌ WRONG (Host Paths)
```
C:\Users\Name\Downloads\model.osm
C:\Users\Name\Documents\output.idf
```

#### ✅ CORRECT (Container Paths)
```
/mnt/c/Users/Name/Downloads/model.osm
/mnt/c/Users/Name/Documents/output.idf
```

### Common Path Mappings

| Your Folder (Windows) | Container Path |
|----------------------|----------------|
| `C:\Users\<Name>\Downloads\` | `/mnt/c/Users/<Name>/Downloads/` |
| `C:\Users\<Name>\Documents\` | `/mnt/c/Users/<Name>/Documents/` |
| `C:\Users\<Name>\Desktop\` | `/mnt/c/Users/<Name>/Desktop/` |
| `C:\Projects\` | `/mnt/c/Projects/` |
| Project samples | `/workspace/openstudio-mcp-server/sample_files/` |

### Example Usage

**Load a model from Downloads:**
```
User: "Load /mnt/c/Users/JohnDoe/Downloads/Office-Building.osm"
```

**Convert and save to Documents:**
```
User: "Convert the model to IDF and save it to /mnt/c/Users/JohnDoe/Documents/Office-Building.idf"
```

**Why This Matters:**
- ✅ Files at `/mnt/c/...` paths persist after container stops
- ❌ Files saved to `/tmp/...` or `/workspace/...` (without `/mnt/c`) are lost

📖 **For complete file access documentation, see [CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md#file-access-pattern)**

---

## Usage

### Basic Workflow

1. **Place your OSM file** in the `sample_files/models/` directory

2. **Ask Claude** to work with it:
   ```
   "Load R2F-Office-Hub-006.osm and tell me about the building"
   ```

3. **Claude will**:
   - Load the model using `load_osm_model`
   - Extract information using `get_model_summary`, `list_spaces`, etc.
   - Present the results in natural language

### Example Conversations

#### Analyze a Building
```
You: "Load the office building model and describe its HVAC systems"

Claude will:
1. Use load_osm_model("office-building.osm")
2. Use list_air_loops()
3. Summarize the HVAC configuration
```

#### Export to EnergyPlus
```
You: "Convert this model to IDF format for simulation"

Claude will:
1. Use convert_to_idf()
2. Report the output file location
```

#### Compare Spaces
```
You: "Which spaces have the highest lighting power density?"

Claude will:
1. Use list_spaces()
2. Use list_lighting_loads()
3. Analyze and rank the results
```

### Working with Uploaded Files

Claude Desktop can handle files you upload directly:

1. Upload your `.osm` file in the chat
2. Ask Claude to analyze it
3. The server automatically finds and loads it from Claude's upload directory

---

## Project Structure

```
openstudio-mcp-server/
├── openstudio_mcp_server/          # Main server package
│   ├── server.py                   # MCP tool definitions
│   ├── openstudio_manager.py       # Business logic layer
│   ├── config.py                   # Configuration management
│   └── utils/
│       ├── path_utils.py           # Intelligent path resolution
│       └── __init__.py
├── openstudio_toolkit/             # OpenStudio Python library
├── sample_files/                   # Example models
│   ├── models/                     # OSM files
│   └── weather/                    # EPW weather files
├── outputs/                        # Generated files (IDF exports, etc.)
├── logs/                           # Server logs
├── .devcontainer/
│   └── Dockerfile                  # Docker container definition
├── pyproject.toml                  # Python dependencies
├── README.md                       # This file
├── USER_GUIDE.md                   # User documentation
└── DEVELOPER_NOTES.md              # Technical documentation
```

---

## Documentation

- **[CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md)** - ⭐ Golden Docker configuration for Claude Desktop
- **[TESTING_PROTOCOL.md](TESTING_PROTOCOL.md)** - Standard testing procedures and troubleshooting
- **[USER_GUIDE.md](USER_GUIDE.md)** - Simple guide for end users (includes smart path handling)
- **[DEVELOPER_NOTES.md](DEVELOPER_NOTES.md)** - Technical implementation details

---

## How It Works

### Architecture

```
User (Claude Desktop)
    ↓
Claude AI (analyzes request, selects tools)
    ↓
MCP Protocol (JSON-RPC over stdin/stdout)
    ↓
FastMCP Server (server.py - tool definitions)
    ↓
OpenStudioManager (openstudio_manager.py - business logic)
    ↓
OpenStudio-Toolkit (Python wrapper functions)
    ↓
OpenStudio SDK (C++ library with Python bindings)
```

### Tool Execution Flow

1. **User asks**: "How many spaces are in this building?"
2. **Claude selects tool**: `list_spaces()`
3. **Server executes**:
   - Checks if model is loaded
   - Calls OpenStudio-Toolkit function
   - Extracts space data into DataFrame
   - Converts to JSON
4. **Returns to Claude**: `{"status": "success", "count": 12, "spaces": [...]}`
5. **Claude responds**: "This building has 12 spaces..."

---

## Development

### Adding New Tools

See [DEVELOPER_NOTES.md](DEVELOPER_NOTES.md) for detailed instructions on:
- Adding new MCP tools
- Integrating OpenStudio-Toolkit functions
- Error handling patterns
- Testing procedures

### Running Tests

```bash
# In Docker container
docker run --rm -i \
  -v "$(pwd):/workspace" \
  openstudio-mcp-dev bash -c "
  cd /workspace && uv run python -m pytest tests/
"
```

### Local Development

```bash
# Install dependencies
uv pip install -e .

# Run server locally
uv run python -m openstudio_mcp_server.server
```

---

## Troubleshooting

### "Model not loaded" Error
- Ensure you've loaded a model first with `load_osm_model`
- Check that the file is in `sample_files/models/`

### "File not found" Error
- Verify the file path is correct
- Check file is in mounted workspace directory
- Try using just the filename (server will search automatically)

### Claude Doesn't Use Tools
- Verify MCP server is connected (check Claude Desktop status bar)
- Restart Claude Desktop
- Check server logs in `logs/openstudio_mcp_server.log`

### Docker Issues
- Ensure Docker Desktop is running
- Verify volume mount path is correct and absolute
- Check Docker image was built successfully

### "ModuleNotFoundError: No module named 'openstudio'" Error
This means the OpenStudio Python bindings are not installed. This should not happen with the Docker image, but if you're running locally:

```bash
# Install OpenStudio Python package
pip install openstudio==3.7.0

# Verify installation
python -c "import openstudio; print(openstudio.openStudioVersion())"
```

**Note**: The Docker image automatically installs this package during build.

---

## Roadmap

Future enhancements planned:

- **Model Modification**: Tools to create and modify spaces, zones, surfaces
- **Advanced HVAC**: Detailed HVAC component inspection and editing
- **Simulation**: Execute EnergyPlus simulations
- **Results Analysis**: Parse and visualize simulation results
- **Parametric Studies**: Automated parametric analysis workflows
- **Geometry Tools**: Create building geometry from scratch

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- **[LBNL-ETA](https://github.com/LBNL-ETA)** for the EnergyPlus MCP Server architecture that served as the foundation for this project
- **[OpenStudio-Toolkit](https://github.com/roruizf/OpenStudio-Toolkit)** for providing the Python interface to OpenStudio
- **[NREL](https://www.nrel.gov/)** for developing and maintaining the OpenStudio SDK
- **[Anthropic](https://www.anthropic.com/)** for Claude and Claude Code (Sonnet 4.5)
- **Model Context Protocol** community for the MCP specification

---

## Support

- **Issues**: [GitHub Issues](https://github.com/roruizf/openstudio-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/roruizf/openstudio-mcp-server/discussions)
- **OpenStudio Documentation**: [https://openstudio.net/](https://openstudio.net/)

---

**Built with ❤️ using Claude Code, Python and OpenStudio**
