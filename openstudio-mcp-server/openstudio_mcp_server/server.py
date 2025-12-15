"""
OpenStudio MCP Server - Main server implementation.

This module defines the MCP server and all available tools for
working with OpenStudio building energy models.
"""

import logging
import json
import sys
from typing import Optional, Any, Union

from mcp.server.fastmcp import FastMCP

from openstudio_mcp_server.config import get_config, get_configuration_info
from openstudio_mcp_server.openstudio_tools import OpenStudioManager
from openstudio_mcp_server.utils.json_utils import ensure_json_response

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
        return ensure_json_response(result)

    except FileNotFoundError as e:
        logger.warning(f"File not found: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error loading OSM file: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": f"Failed to load OSM file: {str(e)}"})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error saving OSM file: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": f"Failed to save OSM file: {str(e)}"})


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
        logger.info(
            f"Tool called: convert_to_idf(output_path='{output_path}')")
        result = os_manager.convert_to_idf(output_path)
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error converting to IDF: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": f"Failed to convert to IDF: {str(e)}"})


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
        result = os_manager.copy_file(
            source_path, target_path, overwrite, file_types)
        return ensure_json_response(result)

    except Exception as e:
        logger.error(f"Error copying file: {e}", exc_info=True)
        return ensure_json_response(
            {"status": "error", "error": f"Failed to copy file: {str(e)}"}
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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error getting model summary: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error getting building info: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing spaces: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        logger.info(
            f"Tool called: get_space_details(space_name='{space_name}')")
        result = os_manager.get_space_by_name(space_name)
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error getting space details: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing thermal zones: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        logger.info(
            f"Tool called: get_thermal_zone_details(zone_name='{zone_name}')")
        result = os_manager.get_thermal_zone_by_name(zone_name)
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error getting thermal zone details: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing materials: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing air loops: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing people loads: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing lighting loads: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing electric equipment: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response(result)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ensure_json_response({"status": "error", "error": str(e)})

    except Exception as e:
        logger.error(f"Error listing schedule rulesets: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
        return ensure_json_response({"status": "success", "configuration": result})

    except Exception as e:
        logger.error(f"Error getting server info: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


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
            return ensure_json_response({
                "status": "success",
                "model_loaded": False,
                "message": "No model currently loaded. Use load_osm_model to load a model."
            })

        return ensure_json_response({
            "status": "success",
            "model_loaded": True,
            "file_path": os_manager.current_file_path,
            "message": "Model is loaded and ready for operations."
        })

    except Exception as e:
        logger.error(f"Error getting model status: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


@mcp.tool()
async def apply_space_type_and_construction_set_wizard(
    building_type: str,
    template: str,
    climate_zone: str,
    create_space_types: bool = True,
    create_construction_set: bool = True,
    set_building_defaults: bool = True,
    model_path: str = None
) -> str:
    """Apply the Space Type and Construction Set Wizard to automatically configure buildings.

    This powerful wizard automatically applies ASHRAE 90.1 or DOE prototype building
    configurations based on building type, energy code template, and climate zone.
    It creates appropriate space types, assigns them to spaces, and configures
    construction sets according to the selected energy code.

    Args:
        building_type: Type of building. Valid options:
            - Schools: "SecondarySchool", "PrimarySchool"
            - Office: "SmallOffice", "MediumOffice", "LargeOffice"
            - Lodging: "SmallHotel", "LargeHotel"
            - Warehouse: "Warehouse"
            - Retail: "RetailStandalone", "RetailStripmall"
            - Food Service: "QuickServiceRestaurant", "FullServiceRestaurant"
            - Residential: "MidriseApartment", "HighriseApartment"
            - Healthcare: "Hospital", "Outpatient"
            - Other: "SuperMarket", "Laboratory", "Courthouse", "College"
            - Data Centers: "LargeDataCenterLowITE", "LargeDataCenterHighITE",
              "SmallDataCenterLowITE", "SmallDataCenterHighITE"

        template: Energy code template. Valid options:
            - DOE Reference: "DOE Ref Pre-1980", "DOE Ref 1980-2004"
            - ASHRAE 90.1: "90.1-2004", "90.1-2007", "90.1-2010", "90.1-2013",
              "90.1-2016", "90.1-2019"
            - ComStock: "ComStock DOE Ref Pre-1980", "ComStock DOE Ref 1980-2004",
              "ComStock 90.1-2004", "ComStock 90.1-2007", "ComStock 90.1-2010",
              "ComStock 90.1-2013", "ComStock 90.1-2016", "ComStock 90.1-2019"

        climate_zone: ASHRAE 169-2013 climate zone. Valid options:
            - Zone 1: "ASHRAE 169-2013-1A", "ASHRAE 169-2013-1B"
            - Zone 2: "ASHRAE 169-2013-2A", "ASHRAE 169-2013-2B"
            - Zone 3: "ASHRAE 169-2013-3A", "ASHRAE 169-2013-3B", "ASHRAE 169-2013-3C"
            - Zone 4: "ASHRAE 169-2013-4A", "ASHRAE 169-2013-4B", "ASHRAE 169-2013-4C"
            - Zone 5: "ASHRAE 169-2013-5A", "ASHRAE 169-2013-5B", "ASHRAE 169-2013-5C"
            - Zone 6: "ASHRAE 169-2013-6A", "ASHRAE 169-2013-6B"
            - Zone 7: "ASHRAE 169-2013-7A"
            - Zone 8: "ASHRAE 169-2013-8A"

        create_space_types: Whether to create and assign space types (default: True)
        create_construction_set: Whether to create construction set (default: True)
        set_building_defaults: Whether to set building defaults using new objects. (default: False)
        model_path: Optional path to model file. If not provided, uses currently loaded model.

    Returns:
        JSON string with wizard status and results including saved file path

    Examples:
        # Apply wizard to current model with small office configuration
        apply_space_type_and_construction_set_wizard("SmallOffice", "90.1-2013", "ASHRAE 169-2013-3A")

        # Apply wizard to a specific model file
        apply_space_type_and_construction_set_wizard("RetailStandalone", "90.1-2019", "ASHRAE 169-2013-5B", model_path="mybuilding.osm")

        # Apply wizard for school, creating only space types
        apply_space_type_and_construction_set_wizard("PrimarySchool", "90.1-2016", "ASHRAE 169-2013-4A", create_construction_set=False)
    """
    try:
        logger.info(f"Tool called: apply_space_type_and_construction_set_wizard(building_type={building_type}, "
                    f"template={template}, climate_zone={climate_zone})")

        result = os_manager.apply_space_type_and_construction_set_wizard(
            building_type=building_type,
            template=template,
            climate_zone=climate_zone,
            create_space_types=create_space_types,
            create_construction_set=create_construction_set,
            set_building_defaults=set_building_defaults,
            model_path=model_path
        )
        return ensure_json_response(result)

    except Exception as e:
        logger.error(f"Error applying Space Type Wizard: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


@mcp.tool()
async def apply_view_model(
    output_filename: str = "model_report.html"
) -> str:
    """Apply the View Model measure to generate an interactive HTML visualization.

    This measure generates a comprehensive HTML report with:
    - 3D geometry visualization
    - Building component breakdown (spaces, zones, surfaces)
    - Space types and thermal zones with color coding
    - HVAC system diagrams
    - Material and construction details
    - Detailed statistics and summaries

    The HTML report is interactive and can be opened in any web browser.

    Args:
        output_filename: Name of the output HTML file (default: "model_report.html").
                        The file will be saved in the outputs/ directory.

    Returns:
        JSON response with status and file path

    Example:
        apply_view_model("my_building_report.html")
    """
    try:
        logger.info(f"Applying View Model measure: {output_filename}")
        result = os_manager.apply_view_model(output_filename=output_filename)
        return ensure_json_response(result)

    except Exception as e:
        logger.error(f"Error applying View Model measure: {e}", exc_info=True)
        return ensure_json_response({"status": "error", "error": str(e)})


# =============================================================================
# MAIN SERVER ENTRY POINT
# =============================================================================


def main():
    """Main entry point for the OpenStudio MCP server."""
    try:
        logger.info("OpenStudio MCP Server starting...")
        logger.info(f"Server: {config.server.name} v{config.server.version}")
        logger.info(
            f"OpenStudio installation: {config.openstudio.installation_dir}")
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
