# OpenStudio MCP Server - User Guide

## What is this?

This server allows AI assistants (like Claude) to work with OpenStudio building energy models. You can ask Claude to analyze, modify, or create building models, and it will use these tools to do the work.

## Quick Start

### 1. Load a Model

Place your `.osm` file in the `sample_files/models/` directory, then ask Claude:

```
"Load the model R2F-Office-Hub-006.osm"
```

Claude will use the `load_osm_model` tool to load it.

### 2. Inspect the Model

Once loaded, you can ask questions like:

```
"How many spaces are in this building?"
"What are the thermal zones?"
"Show me the HVAC systems"
"List all the materials used"
```

Claude will use tools like `list_spaces`, `list_thermal_zones`, `list_air_loops`, and `list_materials`.

### 3. Export to EnergyPlus

To run simulations in EnergyPlus, convert the model:

```
"Convert this model to IDF format"
```

Claude will use the `convert_to_idf` tool.

## Available Tools

### File Operations
- **load_osm_model** - Load an OpenStudio model file
- **save_osm_model** - Save changes to the model
- **convert_to_idf** - Export to EnergyPlus IDF format
- **copy_file** - Copy files between locations

### Building Information
- **get_model_summary** - Overall model statistics
- **get_building_info** - Building object details
- **list_spaces** - All spaces in the building
- **get_space_details** - Specific space information
- **list_thermal_zones** - All thermal zones
- **get_thermal_zone_details** - Specific zone information

### Systems & Loads
- **list_air_loops** - HVAC air systems
- **list_people_loads** - Occupancy definitions
- **list_lighting_loads** - Lighting power densities
- **list_electric_equipment** - Equipment loads

### Materials
- **list_materials** - All construction materials
- **list_schedule_rulesets** - Operating schedules

### Server Status
- **get_server_info** - Server configuration
- **get_current_model_status** - Currently loaded model

## How It Works

1. **You ask Claude** to do something with a building model
2. **Claude selects appropriate tools** based on your request
3. **The MCP server executes the tools** using the OpenStudio library
4. **Results are returned** as JSON data
5. **Claude interprets and presents** the results in natural language

## Working with Files

### How to Open Files

**Smart Path Handling: You can copy the path directly from your Windows Explorer** (e.g., `C:\Users\Name\Downloads\model.osm`) **and paste it into the chat. The server automatically detects and converts it to work inside Docker.**

For example, just tell Claude:
```
"Load the model at C:\Users\John\Documents\MyBuilding.osm"
```

The server will automatically translate this to the Docker path and load your file.

**Alternative Options:**
- **Place files in the workspace**: Copy your `.osm` files to `C:\openstudio-mcp-server\sample_files\models\` before starting
- **Use simple filenames**: If the file is already in the workspace, just use the filename: `"Load model.osm"`

### Saving Files

**Important**: When saving files, use absolute paths to ensure they're saved to the correct location on your Windows host machine.

For example:
```
"Save the modified model to C:\Users\John\Documents\modified_building.osm"
```

This ensures your file is saved where you expect it, not inside the container.

### File Locations

- **Your models**: Place in `sample_files/models/`
- **Weather files**: Place in `sample_files/weather/`
- **Output files**: Generated in `outputs/` (or specify your own path)
- **Logs**: Server logs in `logs/`

## Example Conversations

### Example 1: Basic Analysis

**You**: "Load R2F-Office-Hub-006.osm and tell me about it"

**Claude**: Uses these tools in sequence:
1. `load_osm_model("R2F-Office-Hub-006.osm")`
2. `get_model_summary()`
3. `list_spaces()`
4. `list_thermal_zones()`

Then tells you: "This building has 12 spaces organized into 4 thermal zones..."

### Example 2: HVAC Analysis

**You**: "What HVAC systems are in this building?"

**Claude**: Uses:
1. `list_air_loops()`

Then explains the system configuration.

### Example 3: Export for Simulation

**You**: "Prepare this model for EnergyPlus simulation"

**Claude**: Uses:
1. `convert_to_idf()`

Then confirms the IDF file location.

## Troubleshooting

### "Model not loaded" error
- Make sure you loaded a model first with `load_osm_model`
- Claude should automatically load the model if you mention it

### "File not found" error
- **Windows users**: Copy the full path from File Explorer (e.g., `C:\Users\...\model.osm`) - the server will auto-translate it
- **Already in workspace**: If you placed the file in `sample_files/models/`, just use the filename
- **Check the path**: Verify the file exists at the location you specified
- File names are case-sensitive on Linux

### Claude doesn't use the tools
- Try being more specific: "Use the OpenStudio tools to..."
- Restart Claude Desktop if the server connection is lost

## Tips for Better Results

1. **Be specific** about file names when you have multiple models
2. **Load the model first** before asking questions about it
3. **Ask one thing at a time** for clearer responses
4. **Check the outputs folder** for generated files
5. **Restart Claude** if tools stop working

## Need Help?

- Check server logs in `logs/openstudio_mcp_server.log`
- Verify the Docker container is running
- Make sure the `.osm` file is valid OpenStudio format
- Try restarting Claude Desktop

---

**Ready to start!** Place your model in `sample_files/models/` and ask Claude to analyze it.
