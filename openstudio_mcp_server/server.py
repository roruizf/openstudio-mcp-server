"""
OpenStudio MCP Server - Main server implementation.

This module defines the MCP server and all available tools for
working with OpenStudio building energy models.
"""

import logging
import json
import sys
from typing import Optional

from mcp.server.fastmcp import FastMCP

from openstudio_mcp_server.config import get_config, get_configuration_info
from openstudio_mcp_server.openstudio_manager import OpenStudioManager

# Initialize configuration and logger
config = get_config()
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP(config.server.name)

# Initialize OpenStudio Manager
os_manager = OpenStudioManager(config)

logger.info(f"Starting {config.server.name} v{config.server.version}")


# =============================================================================
# CATEGORY 1: FILE & MODEL MANAGEMENT TOOLS
# =============================================================================


@mcp.tool()
async def load_osm_model(file_path: str, translate_version: bool = True) -> str:
    """Load an OpenStudio Model (OSM) file.

    This tool loads an OSM file into memory and makes it the current working model.
    All subsequent operations will be performed on this model until a different
    model is loaded.

    Args:
        file_path: Path to the OSM file (can be absolute or relative to workspace)
        translate_version: Whether to translate model to current OpenStudio version (default: True)

    Returns:
        JSON string with loading status and model information

    Examples:
        load_osm_model("sample_files/models/example.osm")
        load_osm_model("/path/to/my/model.osm", translate_version=False)
    """
    try:
        logger.info(f"Tool called: load_osm_model(file_path='{file_path}')")
        result = os_manager.load_osm_file(file_path, translate_version)
        return json.dumps(result, indent=2)

    except FileNotFoundError as e:
        logger.warning(f"File not found: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error loading OSM file: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": f"Failed to load OSM file: {str(e)}"}, indent=2)


@mcp.tool()
async def save_osm_model(file_path: Optional[str] = None) -> str:
    """Save the current OpenStudio Model to an OSM file.

    Args:
        file_path: Path where to save the OSM file (optional, defaults to current file path)

    Returns:
        JSON string with save status

    Examples:
        save_osm_model()  # Save to current file path
        save_osm_model("output/modified_model.osm")
    """
    try:
        logger.info(f"Tool called: save_osm_model(file_path='{file_path}')")
        result = os_manager.save_osm_file(file_path)
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error saving OSM file: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": f"Failed to save OSM file: {str(e)}"}, indent=2)


@mcp.tool()
async def convert_to_idf(output_path: Optional[str] = None) -> str:
    """Convert the current OpenStudio Model to EnergyPlus IDF format.

    This tool exports the current OpenStudio model to an EnergyPlus Input Data File (IDF)
    which can be used for simulation in EnergyPlus.

    Args:
        output_path: Path for the output IDF file (optional, auto-generated if not specified)

    Returns:
        JSON string with conversion status and file path

    Examples:
        convert_to_idf()  # Auto-generate output path
        convert_to_idf("output/model.idf")
    """
    try:
        logger.info(f"Tool called: convert_to_idf(output_path='{output_path}')")
        result = os_manager.convert_to_idf(output_path)
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error converting to IDF: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": f"Failed to convert to IDF: {str(e)}"}, indent=2)


@mcp.tool()
async def copy_file(
    source_path: str,
    target_path: str,
    overwrite: bool = False,
    file_types: Optional[list] = None,
) -> str:
    """Copy a file with intelligent path resolution and fuzzy matching.

    This tool helps copy model files (OSM, IDF, etc.) from various locations to the
    workspace. It uses intelligent path resolution that can find files even with
    partial names or typos. This is especially useful for accessing user-uploaded
    files that Claude may not have direct access to.

    The tool searches in multiple locations:
    - Workspace root directory
    - Sample files directory
    - Models subdirectory
    - Output directory

    Args:
        source_path: Source file path (can be:
                    - Absolute path: "/full/path/to/file.osm"
                    - Relative path: "models/mymodel.osm"
                    - Filename only: "example.osm" (searches in known directories)
                    - Partial name: Uses fuzzy matching to find similar files)
        target_path: Target file path (same flexibility as source_path)
        overwrite: Whether to overwrite existing target file (default: False)
        file_types: Optional list of valid file extensions (e.g., [".osm", ".idf"])

    Returns:
        JSON string with copy status, resolved paths, and file information

    Examples:
        # Copy a specific OSM file
        copy_file("example.osm", "my_model.osm", file_types=[".osm"])

        # Copy with fuzzy matching (finds similar files)
        copy_file("office", "my_office.osm", file_types=[".osm"])

        # Copy and overwrite existing file
        copy_file("source.osm", "target.osm", overwrite=True)

        # Copy user-uploaded file to workspace
        copy_file("/mnt/user-data/uploads/model.osm", "workspace/model.osm")
    """
    try:
        logger.info(
            f"Tool called: copy_file(source='{source_path}', target='{target_path}', "
            f"overwrite={overwrite}, file_types={file_types})"
        )
        result = os_manager.copy_file(source_path, target_path, overwrite, file_types)
        return json.dumps(result, indent=2)

    except Exception as e:
        logger.error(f"Error copying file: {e}", exc_info=True)
        return json.dumps(
            {"status": "error", "error": f"Failed to copy file: {str(e)}"},
            indent=2
        )


@mcp.tool()
async def get_model_summary() -> str:
    """Get a comprehensive summary of the current OpenStudio model.

    Returns statistics about the model including counts of spaces, thermal zones,
    materials, and other key objects.

    Returns:
        JSON string with model statistics

    Examples:
        get_model_summary()
    """
    try:
        logger.info("Tool called: get_model_summary()")
        result = os_manager.get_model_summary()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error getting model summary: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


@mcp.tool()
async def get_building_info() -> str:
    """Get building object information from the current model.

    Returns details about the building including name, north axis, floor area,
    and associated default construction and schedule sets.

    Returns:
        JSON string with building information

    Examples:
        get_building_info()
    """
    try:
        logger.info("Tool called: get_building_info()")
        result = os_manager.get_building_info()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error getting building info: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# =============================================================================
# CATEGORY 2: BUILDING GEOMETRY INSPECTION TOOLS
# =============================================================================


@mcp.tool()
async def list_spaces() -> str:
    """List all spaces in the current OpenStudio model.

    Returns a comprehensive list of all spaces with their properties including
    name, floor area, volume, thermal zone assignment, and space type.

    Returns:
        JSON string with count and list of all spaces

    Examples:
        list_spaces()
    """
    try:
        logger.info("Tool called: list_spaces()")
        result = os_manager.get_all_spaces()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing spaces: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


@mcp.tool()
async def get_space_details(space_name: str) -> str:
    """Get detailed information about a specific space.

    Args:
        space_name: Name of the space to retrieve

    Returns:
        JSON string with detailed space information

    Examples:
        get_space_details("Office 101")
    """
    try:
        logger.info(f"Tool called: get_space_details(space_name='{space_name}')")
        result = os_manager.get_space_by_name(space_name)
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error getting space details: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


@mcp.tool()
async def list_thermal_zones() -> str:
    """List all thermal zones in the current OpenStudio model.

    Returns a comprehensive list of all thermal zones with their properties including
    name, multiplier, HVAC equipment, and associated spaces.

    Returns:
        JSON string with count and list of all thermal zones

    Examples:
        list_thermal_zones()
    """
    try:
        logger.info("Tool called: list_thermal_zones()")
        result = os_manager.get_all_thermal_zones()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing thermal zones: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


@mcp.tool()
async def get_thermal_zone_details(zone_name: str) -> str:
    """Get detailed information about a specific thermal zone.

    Args:
        zone_name: Name of the thermal zone to retrieve

    Returns:
        JSON string with detailed zone information

    Examples:
        get_thermal_zone_details("Zone 1")
    """
    try:
        logger.info(f"Tool called: get_thermal_zone_details(zone_name='{zone_name}')")
        result = os_manager.get_thermal_zone_by_name(zone_name)
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error getting thermal zone details: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# =============================================================================
# CATEGORY 3: MATERIALS & CONSTRUCTIONS TOOLS
# =============================================================================


@mcp.tool()
async def list_materials() -> str:
    """List all materials in the current OpenStudio model.

    Returns a list of all opaque materials (both standard and massless) with
    their thermal properties including conductivity, density, specific heat,
    and thermal resistance.

    Returns:
        JSON string with count and list of all materials

    Examples:
        list_materials()
    """
    try:
        logger.info("Tool called: list_materials()")
        result = os_manager.get_all_materials()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing materials: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# =============================================================================
# CATEGORY 4: HVAC SYSTEMS TOOLS
# =============================================================================


@mcp.tool()
async def list_air_loops() -> str:
    """List all air loop HVAC systems in the current OpenStudio model.

    Returns a list of all air loops with their properties including supply and
    return air flow rates, availability schedules, and node connections.

    Returns:
        JSON string with count and list of all air loops

    Examples:
        list_air_loops()
    """
    try:
        logger.info("Tool called: list_air_loops()")
        result = os_manager.get_all_air_loops()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing air loops: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# =============================================================================
# CATEGORY 5: INTERNAL LOADS TOOLS
# =============================================================================


@mcp.tool()
async def list_people_loads() -> str:
    """List all people (occupancy) loads in the current OpenStudio model.

    Returns a list of all people objects with their properties including number
    of people, people per floor area, schedules, and activity levels.

    Returns:
        JSON string with count and list of all people loads

    Examples:
        list_people_loads()
    """
    try:
        logger.info("Tool called: list_people_loads()")
        result = os_manager.get_all_people_loads()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing people loads: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


@mcp.tool()
async def list_lighting_loads() -> str:
    """List all lighting loads in the current OpenStudio model.

    Returns a list of all lights objects with their properties including lighting
    power density, schedules, and return air fractions.

    Returns:
        JSON string with count and list of all lighting loads

    Examples:
        list_lighting_loads()
    """
    try:
        logger.info("Tool called: list_lighting_loads()")
        result = os_manager.get_all_lighting_loads()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing lighting loads: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


@mcp.tool()
async def list_electric_equipment() -> str:
    """List all electric equipment loads in the current OpenStudio model.

    Returns a list of all electric equipment objects with their properties including
    power density, schedules, and heat gain fractions.

    Returns:
        JSON string with count and list of all electric equipment

    Examples:
        list_electric_equipment()
    """
    try:
        logger.info("Tool called: list_electric_equipment()")
        result = os_manager.get_all_electric_equipment()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing electric equipment: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# =============================================================================
# CATEGORY 6: SCHEDULES TOOLS
# =============================================================================


@mcp.tool()
async def list_schedule_rulesets() -> str:
    """List all schedule rulesets in the current OpenStudio model.

    Returns a list of all schedule rulesets with their properties including
    schedule type limits and default day schedules.

    Returns:
        JSON string with count and list of all schedule rulesets

    Examples:
        list_schedule_rulesets()
    """
    try:
        logger.info("Tool called: list_schedule_rulesets()")
        result = os_manager.get_all_schedule_rulesets()
        return json.dumps(result, indent=2)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return json.dumps({"status": "error", "error": str(e)}, indent=2)

    except Exception as e:
        logger.error(f"Error listing schedule rulesets: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# =============================================================================
# CATEGORY 7: SERVER MANAGEMENT TOOLS
# =============================================================================


@mcp.tool()
async def get_server_info() -> str:
    """Get OpenStudio MCP server information and configuration.

    Returns server version, configuration paths, OpenStudio installation details,
    and current server settings.

    Returns:
        JSON string with server configuration information

    Examples:
        get_server_info()
    """
    try:
        logger.info("Tool called: get_server_info()")
        result = get_configuration_info(config)
        return json.dumps({"status": "success", "configuration": result}, indent=2)

    except Exception as e:
        logger.error(f"Error getting server info: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


@mcp.tool()
async def get_current_model_status() -> str:
    """Get status of the currently loaded model.

    Returns information about whether a model is loaded, its file path,
    and basic statistics.

    Returns:
        JSON string with current model status

    Examples:
        get_current_model_status()
    """
    try:
        logger.info("Tool called: get_current_model_status()")

        if os_manager.current_model is None:
            return json.dumps({
                "status": "success",
                "model_loaded": False,
                "message": "No model currently loaded. Use load_osm_model to load a model."
            }, indent=2)

        return json.dumps({
            "status": "success",
            "model_loaded": True,
            "file_path": os_manager.current_file_path,
            "message": "Model is loaded and ready for operations."
        }, indent=2)

    except Exception as e:
        logger.error(f"Error getting model status: {e}", exc_info=True)
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# =============================================================================
# MAIN SERVER ENTRY POINT
# =============================================================================


def main():
    """Main entry point for the OpenStudio MCP server."""
    try:
        logger.info("OpenStudio MCP Server starting...")
        logger.info(f"Server: {config.server.name} v{config.server.version}")
        logger.info(f"OpenStudio installation: {config.openstudio.installation_dir}")
        logger.info(f"Workspace: {config.paths.workspace_root}")

        # Run the server with stdio transport
        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Fatal error in server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
