# OpenStudio MCP Server

A **Model Context Protocol (MCP)** server that enables AI assistants like Claude to interact with **OpenStudio** building energy models. Load, inspect, and manipulate OpenStudio Model (OSM) files through a comprehensive set of tools accessible via natural language.

## Credits and Acknowledgments

This project is heavily based on the [**EnergyPlus MCP Server**](https://github.com/LBNL-ETA/energyplus-mcp) developed by **LBNL-ETA** (Lawrence Berkeley National Laboratory - Energy Technologies Area). The server architecture, tool structure, and implementation patterns have been replicated as closely as possible from their excellent work.

The tools in this server are built using the [**OpenStudio-Toolkit**](https://github.com/roruizf/OpenStudio-Toolkit) library, which provides Python interfaces to OpenStudio's building modeling capabilities.

This project was developed with the invaluable assistance of **Claude Code** powered by **Anthropic's Claude Sonnet 4.5**.

---

## Features

### Available Tools (19+)

####📁 **File & Model Management**
- `load_osm_model` - Load OpenStudio Model files with intelligent path resolution
- `save_osm_model` - Save modified models
- `convert_to_idf` - Export to EnergyPlus IDF format
- `copy_file` - Copy files with fuzzy matching and smart discovery
- `get_model_summary` - Get comprehensive model statistics
- `get_building_info` - Get building object details

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

- **Python 3.10+**
- **Docker Desktop** (for containerized deployment)
- **OpenStudio 3.7.0** (installed in Docker container)
- **Claude Desktop**, **VS Code**, or **Cursor** (for AI assistant integration)

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/roruizf/openstudio-mcp-server.git
cd openstudio-mcp-server
```

#### 2. Build Docker Image

```bash
docker build -t openstudio-mcp-dev -f .devcontainer/Dockerfile .
```

This builds a container with:
- Python 3.12
- OpenStudio 3.7.0
- All required dependencies
- OpenStudio-Toolkit library

#### 3. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "openstudio": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "/absolute/path/to/openstudio-mcp-server:/workspace",
        "-w",
        "/workspace",
        "openstudio-mcp-dev",
        "uv",
        "run",
        "python",
        "-m",
        "openstudio_mcp_server.server"
      ]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/openstudio-mcp-server` with your actual path:
- **macOS/Linux**: `/Users/username/openstudio-mcp-server`
- **Windows**: `C:\openstudio-mcp-server` (use forward slashes in JSON)

#### 4. Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

#### 5. Verify Installation

In Claude Desktop, ask:
```
"What OpenStudio tools are available?"
```

Claude should list all available tools.

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
├── DEVELOPER_NOTES.md              # Technical documentation
└── FILE_ACCESS_GUIDE.md            # File handling details
```

---

## Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Simple guide for end users
- **[DEVELOPER_NOTES.md](DEVELOPER_NOTES.md)** - Technical implementation details
- **[FILE_ACCESS_GUIDE.md](FILE_ACCESS_GUIDE.md)** - How file discovery works
- **[CLAUDE_DESKTOP_FIX.md](CLAUDE_DESKTOP_FIX.md)** - Claude Desktop integration notes

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

## Citation

If you use this software in your research, please cite:

```bibtex
@software{openstudio_mcp_server,
  author = {Ruiz, Rodrigo},
  title = {OpenStudio MCP Server},
  year = {2024},
  url = {https://github.com/roruizf/openstudio-mcp-server},
  note = {Based on EnergyPlus MCP Server by LBNL-ETA}
}
```

Also please cite the original EnergyPlus MCP Server:

```bibtex
@software{energyplus_mcp_server,
  author = {{LBNL-ETA}},
  title = {EnergyPlus MCP Server},
  year = {2024},
  url = {https://github.com/LBNL-ETA/energyplus-mcp}
}
```

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

**Built with ❤️ using Claude Code and OpenStudio**
