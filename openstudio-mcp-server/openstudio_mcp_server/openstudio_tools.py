"""
OpenStudio Manager - Core orchestration layer for MCP tools.

This module provides state management and high-level methods for
interacting with OpenStudio models through the OpenStudio-Toolkit.
"""

import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import os
import shutil
from datetime import datetime

# Import path utilities
from .utils.path_utils import resolve_osm_path, resolve_idf_path, resolve_output_path

# Import openstudio-toolkit functions
from openstudio_toolkit.tasks.measures.apply_space_type_and_construction_set_wizard import (
    run as run_apply_space_type_and_construction_set_wizard,
    validator as validate_apply_space_type_and_construction_set_wizard
)

logger = logging.getLogger(__name__)


class OpenStudioManager:
    """
    Manager class for OpenStudio model operations.

    This class maintains state (current model) and provides high-level
    methods that wrap the OpenStudio-Toolkit functions for use by MCP tools.
    """

    def __init__(self, config):
        """
        Initialize the OpenStudio Manager.

        Args:
            config: Configuration object with paths and settings
        """
        self.config = config
        self.current_model = None
        self.current_file_path = None
        self.logger = logging.getLogger(__name__)

        self.logger.info("OpenStudioManager initialized")
        self.logger.info(
            f"OpenStudio installation: {config.openstudio.installation_dir}")

    # =========================================================================
    # FILE OPERATIONS
    # =========================================================================

    def load_osm_file(self, file_path: str, translate_version: bool = True) -> Dict[str, Any]:
        """
        Load an OpenStudio Model (OSM) file.

        Args:
            file_path: Path to the OSM file (absolute or relative)
            translate_version: Whether to translate to current OpenStudio version

        Returns:
            Dictionary with model information and status

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file cannot be loaded
        """
        try:
            # Resolve file path using intelligent path resolution (NO CACHE - dynamic search)
            resolved_path = resolve_osm_path(self.config, file_path)

            # Verify file exists and log file info for debugging
            if not os.path.exists(resolved_path):
                raise FileNotFoundError(
                    f"OSM file not found after resolution: {resolved_path}")

            file_size = os.path.getsize(resolved_path)
            file_mtime = os.path.getmtime(resolved_path)
            self.logger.info(
                f"Loading OSM file: {resolved_path} ({file_size} bytes, modified: {file_mtime})")

            # Import toolkit function
            from openstudio_toolkit.utils.osm_utils import load_osm_file_as_model

            # Load the model - ALWAYS reads from disk (no cache)
            model = load_osm_file_as_model(
                osm_file_path=resolved_path,
                version_translator=translate_version
            )

            if model is None:
                raise ValueError(f"Failed to load OSM file: {resolved_path}")

            # Update state with NEW model (replaces any previous model)
            self.current_model = model
            self.current_file_path = resolved_path

            self.logger.info(
                f"Model loaded successfully from: {resolved_path}")

            # Get building info
            building_info = self._get_building_summary()

            self.logger.info(
                f"Successfully loaded model: {building_info.get('name', 'Unnamed')}")

            return {
                "status": "success",
                "message": f"Successfully loaded OSM file: {os.path.basename(resolved_path)}",
                "file_path": resolved_path,
                "model_info": building_info,
            }

        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading OSM file: {e}")
            raise ValueError(f"Failed to load OSM file: {str(e)}")

    def save_osm_file(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Save the current OpenStudio Model to an OSM file.

        Args:
            file_path: Path where to save (optional, defaults to current file path)

        Returns:
            Dictionary with save status

        Raises:
            ValueError: If no model is loaded or save fails
        """
        try:
            if self.current_model is None:
                raise ValueError("No model loaded. Load a model first.")

            # Determine save path
            if file_path is None:
                if self.current_file_path is None:
                    raise ValueError(
                        "No file path specified and no current file path")
                save_path = self.current_file_path
            else:
                save_path = resolve_output_path(
                    self.config, file_path, file_types=['.osm'])

            self.logger.info(f"Saving OSM file: {save_path}")

            # Import toolkit function
            from openstudio_toolkit.utils.osm_utils import save_model_as_osm_file

            # Save the model
            save_model_as_osm_file(
                osm_model=self.current_model,
                osm_file_path=save_path
            )

            # Update current path
            self.current_file_path = save_path

            self.logger.info(f"Successfully saved model to: {save_path}")

            return {
                "status": "success",
                "message": f"Successfully saved OSM file: {os.path.basename(save_path)}",
                "file_path": save_path,
            }

        except Exception as e:
            self.logger.error(f"Error saving OSM file: {e}")
            raise ValueError(f"Failed to save OSM file: {str(e)}")

    def convert_to_idf(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert the current OpenStudio Model to EnergyPlus IDF format.

        Args:
            output_path: Path for the IDF file (optional)

        Returns:
            Dictionary with conversion status

        Raises:
            ValueError: If no model is loaded or conversion fails
        """
        try:
            if self.current_model is None:
                raise ValueError("No model loaded. Load a model first.")

            # Determine output path
            if output_path is None:
                if self.current_file_path is None:
                    output_path = os.path.join(
                        self.config.paths.output_dir, "model.idf")
                else:
                    base_name = os.path.splitext(
                        os.path.basename(self.current_file_path))[0]
                    output_path = os.path.join(
                        self.config.paths.output_dir, f"{base_name}.idf")
            else:
                output_path = resolve_output_path(
                    self.config, output_path, file_types=['.idf'])

            self.logger.info(f"Converting OSM to IDF: {output_path}")

            # Import toolkit function
            from openstudio_toolkit.utils.osm_utils import convert_osm_to_idf

            # Convert the model
            convert_osm_to_idf(
                osm_model=self.current_model,
                idf_file_path=output_path
            )

            self.logger.info(f"Successfully converted to IDF: {output_path}")

            return {
                "status": "success",
                "message": f"Successfully converted to IDF: {os.path.basename(output_path)}",
                "file_path": output_path,
            }

        except Exception as e:
            self.logger.error(f"Error converting to IDF: {e}")
            raise ValueError(f"Failed to convert to IDF: {str(e)}")

    def copy_file(
        self,
        source_path: str,
        target_path: str,
        overwrite: bool = False,
        file_types: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Copy a file with intelligent path resolution and validation.

        This method helps users copy model files (OSM, IDF, etc.) from various
        locations to the workspace, with fuzzy matching to find files even with
        partial names or typos.

        Args:
            source_path: Source file path (can be absolute, relative, or just filename)
            target_path: Target file path (can be absolute, relative, or just filename)
            overwrite: Whether to overwrite existing target file
            file_types: Optional list of valid file extensions (e.g., ['.osm', '.idf'])

        Returns:
            Dictionary with copy status and file information

        Raises:
            FileNotFoundError: If source file not found
            FileExistsError: If target exists and overwrite=False
            PermissionError: If cannot read source or write target
        """
        from .utils.path_utils import resolve_path

        try:
            start_time = datetime.now()

            # Resolve source path (must exist)
            self.logger.info(f"Resolving source file: {source_path}")
            resolved_source = resolve_path(
                self.config,
                source_path,
                file_types=file_types,
                description="source file",
                must_exist=True,
                enable_fuzzy_matching=True,
            )

            # Check source is readable
            if not os.access(resolved_source, os.R_OK):
                raise PermissionError(
                    f"Cannot read source file: {resolved_source}")

            # Get source file info
            source_size = os.path.getsize(resolved_source)
            self.logger.info(
                f"Source file resolved: {resolved_source} ({source_size:,} bytes)"
            )

            # Resolve target path (can create)
            self.logger.info(f"Resolving target file: {target_path}")
            resolved_target = resolve_path(
                self.config,
                target_path,
                file_types=file_types,
                description="target file",
                must_exist=False,
            )

            # Check if target already exists
            if os.path.exists(resolved_target) and not overwrite:
                raise FileExistsError(
                    f"Target file already exists: {resolved_target}\n"
                    f"Use overwrite=True to replace it."
                )

            # Create target directory if needed
            target_dir = os.path.dirname(resolved_target)
            if target_dir:
                try:
                    os.makedirs(target_dir, exist_ok=True)
                except (PermissionError, OSError) as e:
                    raise PermissionError(
                        f"Cannot create target directory: {target_dir}\n{e}")

            # Perform the copy
            self.logger.info(
                f"Copying file: {resolved_source} -> {resolved_target}")
            # Preserves metadata
            shutil.copy2(resolved_source, resolved_target)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Verify the copy
            if not os.path.exists(resolved_target):
                raise IOError(
                    "Copy operation completed but target file not found")

            target_size = os.path.getsize(resolved_target)
            if source_size != target_size:
                raise IOError(
                    f"File size mismatch after copy: "
                    f"source={source_size:,} bytes, target={target_size:,} bytes"
                )

            self.logger.info(
                f"Successfully copied file ({target_size:,} bytes) in {duration:.2f}s"
            )

            return {
                "status": "success",
                "message": f"Successfully copied file",
                "source": {
                    "original_path": source_path,
                    "resolved_path": resolved_source,
                    "size_bytes": source_size,
                },
                "target": {
                    "original_path": target_path,
                    "resolved_path": resolved_target,
                    "size_bytes": target_size,
                },
                "copy_duration_seconds": duration,
            }

        except FileNotFoundError as e:
            # Try to provide suggestions
            self.logger.error(f"Source file not found: {e}")
            error_msg = str(e)
            return {
                "status": "error",
                "error": error_msg,
                "original_paths": {
                    "source": source_path,
                    "target": target_path,
                },
            }

        except FileExistsError as e:
            self.logger.warning(f"Target file exists: {e}")
            return {
                "status": "error",
                "error": str(e),
                "suggestion": "Use overwrite=True parameter to replace the existing file",
            }

        except PermissionError as e:
            self.logger.error(f"Permission error: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

        except Exception as e:
            self.logger.error(f"Error copying file: {e}")
            return {
                "status": "error",
                "error": f"Failed to copy file: {str(e)}",
            }

    # =========================================================================
    # MODEL INSPECTION - BUILDING & GEOMETRY
    # =========================================================================

    def get_building_info(self) -> Dict[str, Any]:
        """
        Get building object information.

        Returns:
            Dictionary with building information

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.building import get_building_object_as_dataframe

            df = get_building_object_as_dataframe(self.current_model)

            if len(df) > 0:
                building_dict = df.to_dict(orient='records')[0]
            else:
                building_dict = {}

            return {
                "status": "success",
                "building": building_dict,
            }

        except Exception as e:
            self.logger.error(f"Error getting building info: {e}")
            raise ValueError(f"Failed to get building info: {str(e)}")

    def get_all_spaces(self) -> Dict[str, Any]:
        """
        Get all spaces from the current model.

        Returns:
            Dictionary with space count and list of spaces

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.spaces import get_all_space_objects_as_dataframe

            df = get_all_space_objects_as_dataframe(self.current_model)
            spaces = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(spaces),
                "spaces": spaces,
            }

        except Exception as e:
            self.logger.error(f"Error getting spaces: {e}")
            raise ValueError(f"Failed to get spaces: {str(e)}")

    def get_space_by_name(self, space_name: str) -> Dict[str, Any]:
        """
        Get details for a specific space by name.

        Args:
            space_name: Name of the space

        Returns:
            Dictionary with space details

        Raises:
            ValueError: If no model is loaded or space not found
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.spaces import get_space_object_as_dict

            space_dict = get_space_object_as_dict(
                self.current_model,
                space_name=space_name
            )

            return {
                "status": "success",
                "space": space_dict,
            }

        except Exception as e:
            self.logger.error(f"Error getting space '{space_name}': {e}")
            raise ValueError(f"Failed to get space: {str(e)}")

    def get_all_thermal_zones(self) -> Dict[str, Any]:
        """
        Get all thermal zones from the current model.

        Returns:
            Dictionary with zone count and list of zones

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.thermal_zones import (
                get_all_thermal_zones_objects_as_dataframe
            )

            df = get_all_thermal_zones_objects_as_dataframe(self.current_model)
            zones = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(zones),
                "thermal_zones": zones,
            }

        except Exception as e:
            self.logger.error(f"Error getting thermal zones: {e}")
            raise ValueError(f"Failed to get thermal zones: {str(e)}")

    def get_thermal_zone_by_name(self, zone_name: str) -> Dict[str, Any]:
        """
        Get details for a specific thermal zone by name.

        Args:
            zone_name: Name of the thermal zone

        Returns:
            Dictionary with zone details

        Raises:
            ValueError: If no model is loaded or zone not found
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.thermal_zones import (
                get_thermal_zone_object_as_dict
            )

            zone_dict = get_thermal_zone_object_as_dict(
                self.current_model,
                zone_name=zone_name
            )

            return {
                "status": "success",
                "thermal_zone": zone_dict,
            }

        except Exception as e:
            self.logger.error(f"Error getting thermal zone '{zone_name}': {e}")
            raise ValueError(f"Failed to get thermal zone: {str(e)}")

    # =========================================================================
    # MODEL INSPECTION - MATERIALS & CONSTRUCTIONS
    # =========================================================================

    def get_all_materials(self) -> Dict[str, Any]:
        """
        Get all materials from the current model.

        Returns:
            Dictionary with material count and list of materials

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.materials import (
                get_all_opaque_material_objects_as_dataframe
            )

            df = get_all_opaque_material_objects_as_dataframe(
                self.current_model)
            materials = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(materials),
                "materials": materials,
            }

        except Exception as e:
            self.logger.error(f"Error getting materials: {e}")
            raise ValueError(f"Failed to get materials: {str(e)}")

    # =========================================================================
    # MODEL INSPECTION - HVAC
    # =========================================================================

    def get_all_air_loops(self) -> Dict[str, Any]:
        """
        Get all air loop HVAC systems from the current model.

        Returns:
            Dictionary with air loop count and list of loops

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.hvac_air_loops import (
                get_all_air_loop_hvac_objects_as_dataframe
            )

            df = get_all_air_loop_hvac_objects_as_dataframe(self.current_model)
            air_loops = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(air_loops),
                "air_loops": air_loops,
            }

        except Exception as e:
            self.logger.error(f"Error getting air loops: {e}")
            raise ValueError(f"Failed to get air loops: {str(e)}")

    # =========================================================================
    # MODEL INSPECTION - LOADS
    # =========================================================================

    def get_all_people_loads(self) -> Dict[str, Any]:
        """
        Get all people (occupancy) loads from the current model.

        Returns:
            Dictionary with people load count and list

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.loads import (
                get_all_people_objects_as_dataframe
            )

            df = get_all_people_objects_as_dataframe(self.current_model)
            people = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(people),
                "people_loads": people,
            }

        except Exception as e:
            self.logger.error(f"Error getting people loads: {e}")
            raise ValueError(f"Failed to get people loads: {str(e)}")

    def get_all_lighting_loads(self) -> Dict[str, Any]:
        """
        Get all lighting loads from the current model.

        Returns:
            Dictionary with lighting load count and list

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.loads import (
                get_all_lights_objects_as_dataframe
            )

            df = get_all_lights_objects_as_dataframe(self.current_model)
            lights = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(lights),
                "lighting_loads": lights,
            }

        except Exception as e:
            self.logger.error(f"Error getting lighting loads: {e}")
            raise ValueError(f"Failed to get lighting loads: {str(e)}")

    def get_all_electric_equipment(self) -> Dict[str, Any]:
        """
        Get all electric equipment loads from the current model.

        Returns:
            Dictionary with equipment count and list

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.loads import (
                get_all_electric_equipment_objects_as_dataframe
            )

            df = get_all_electric_equipment_objects_as_dataframe(
                self.current_model)
            equipment = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(equipment),
                "electric_equipment": equipment,
            }

        except Exception as e:
            self.logger.error(f"Error getting electric equipment: {e}")
            raise ValueError(f"Failed to get electric equipment: {str(e)}")

    # =========================================================================
    # MODEL INSPECTION - SCHEDULES
    # =========================================================================

    def get_all_schedule_rulesets(self) -> Dict[str, Any]:
        """
        Get all schedule rulesets from the current model.

        Returns:
            Dictionary with schedule count and list

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            from openstudio_toolkit.osm_objects.schedules import (
                get_all_schedule_ruleset_objects_as_dataframe
            )

            df = get_all_schedule_ruleset_objects_as_dataframe(
                self.current_model)
            schedules = df.to_dict(orient='records')

            return {
                "status": "success",
                "count": len(schedules),
                "schedule_rulesets": schedules,
            }

        except Exception as e:
            self.logger.error(f"Error getting schedule rulesets: {e}")
            raise ValueError(f"Failed to get schedule rulesets: {str(e)}")

    # =========================================================================
    # SPACE TYPE AND CONSTRUCTION SET WIZARD
    # =========================================================================

    def apply_space_type_and_construction_set_wizard(
        self,
        building_type: str,
        template: str,
        climate_zone: str,
        create_space_types: bool = True,
        create_construction_set: bool = True,
        set_building_defaults: bool = True,
        model_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Apply the Space Type and Construction Set Wizard to automatically configure buildings.

        This wizard applies ASHRAE 90.1 or DOE prototype building configurations
        based on building type, template, and climate zone.

        Args:
            building_type: Type of building (e.g., "Office", "Retail", "School")
            template: Energy code template (e.g., "90.1-2013", "90.1-2019")
            climate_zone: ASHRAE climate zone (e.g., "3A", "5B")
            create_space_types: Whether to create and assign space types (default: True)
            create_construction_set: Whether to create construction set (default: True)
            model_path: Optional path to model file (if None, uses current model)

        Returns:
            Dictionary with wizard status and results

        Raises:
            ValueError: If validation fails or wizard execution fails
        """
        try:
            # Step 1: Resolve model path or use current model
            if model_path:
                resolved_path = resolve_osm_path(self.config, model_path)
                # Load the model
                from openstudio_toolkit.utils.osm_utils import load_osm_file_as_model
                model = load_osm_file_as_model(
                    resolved_path, translate_version=True)
                self.logger.info(f"Loaded model from: {resolved_path}")
            else:
                self._check_model_loaded()
                model = self.current_model
                resolved_path = self.current_file_path
                self.logger.info("Using current loaded model")

            # Step 2: Prepare arguments for wizard
            wizard_args = {
                "building_type": building_type,
                "template": template,
                "climate_zone": climate_zone,
                "create_space_types": create_space_types,
                "create_construction_set": create_construction_set,
                "set_building_defaults": set_building_defaults,
            }

            # Step 3: Validate arguments
            self.logger.info(f"Validating wizard arguments: {wizard_args}")
            is_valid = validate_apply_space_type_and_construction_set_wizard(
                model, **wizard_args)

            if not is_valid:
                raise ValueError(
                    f"Invalid wizard arguments. "
                    f"Building type: {building_type}, Template: {template}, "
                    f"Climate zone: {climate_zone}"
                )

            # Step 4: Run the wizard
            self.logger.info("Running Space Type Wizard...")
            updated_model = run_apply_space_type_and_construction_set_wizard(
                model, **wizard_args)

            # Step 5: Update current model
            self.current_model = updated_model

            # Step 6: Save the model to disk
            if resolved_path:
                save_result = self.save_osm_file(resolved_path)
                saved_path = save_result.get("file_path", resolved_path)
            else:
                # If no path, save to outputs with timestamped name
                output_filename = f"wizard_applied_{datetime.now().strftime('%Y%m%d_%H%M%S')}.osm"
                output_path = resolve_output_path(self.config, output_filename)
                save_result = self.save_osm_file(output_path)
                saved_path = save_result.get("file_path", output_path)
                self.current_file_path = saved_path

            self.logger.info(
                f"Wizard applied successfully. Model saved to: {saved_path}")

            return {
                "status": "success",
                "message": f"Space Type and Construction Set Wizard applied successfully",
                "building_type": building_type,
                "template": template,
                "climate_zone": climate_zone,
                "space_types_created": create_space_types,
                "construction_set_created": create_construction_set,
                "model_saved_to": saved_path,
            }

        except Exception as e:
            self.logger.error(
                f"Error applying Space Type and Construction Set Wizard: {e}")
            raise ValueError(
                f"Failed to apply Space Type and Construction Set Wizard: {str(e)}")

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def _check_model_loaded(self) -> None:
        """Check if a model is currently loaded.

        Raises:
            ValueError: If no model is loaded
        """
        if self.current_model is None:
            raise ValueError(
                "No model loaded. Please load an OSM file first using load_osm_model."
            )

    def _resolve_file_path(self, file_path: str) -> str:
        """
        Resolve a file path (handle relative paths, sample files, etc.).

        Args:
            file_path: Input file path

        Returns:
            Absolute file path
        """
        # If already absolute, return as-is
        if os.path.isabs(file_path):
            return file_path

        # Check in workspace root
        workspace_path = os.path.join(
            self.config.paths.workspace_root, file_path)
        if os.path.exists(workspace_path):
            return workspace_path

        # Check in sample files
        sample_path = os.path.join(
            self.config.paths.sample_files_path, file_path)
        if os.path.exists(sample_path):
            return sample_path

        # Check in models subdirectory
        models_path = os.path.join(
            self.config.paths.sample_files_path, "models", file_path)
        if os.path.exists(models_path):
            return models_path

        # Return original path (will fail later if doesn't exist)
        return file_path

    def _get_building_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the building object.

        Returns:
            Dictionary with building summary
        """
        try:
            from openstudio_toolkit.osm_objects.building import get_building_object_as_dataframe

            df = get_building_object_as_dataframe(self.current_model)
            if len(df) > 0:
                return df.to_dict(orient='records')[0]
            return {}
        except Exception as e:
            self.logger.warning(f"Could not get building summary: {e}")
            return {}

    def get_model_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of the current model.

        Returns:
            Dictionary with model statistics

        Raises:
            ValueError: If no model is loaded
        """
        self._check_model_loaded()

        try:
            summary = {
                "status": "success",
                "file_path": self.current_file_path,
                "statistics": {}
            }

            # Get counts of various objects
            try:
                spaces_result = self.get_all_spaces()
                summary["statistics"]["spaces"] = spaces_result["count"]
            except:
                summary["statistics"]["spaces"] = 0

            try:
                zones_result = self.get_all_thermal_zones()
                summary["statistics"]["thermal_zones"] = zones_result["count"]
            except:
                summary["statistics"]["thermal_zones"] = 0

            try:
                materials_result = self.get_all_materials()
                summary["statistics"]["materials"] = materials_result["count"]
            except:
                summary["statistics"]["materials"] = 0

            return summary

        except Exception as e:
            self.logger.error(f"Error getting model summary: {e}")
            raise ValueError(f"Failed to get model summary: {str(e)}")
