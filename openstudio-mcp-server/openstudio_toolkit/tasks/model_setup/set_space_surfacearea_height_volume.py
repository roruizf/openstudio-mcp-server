# src/openstudio_toolkit/tasks/model_setup/set_space_data.py

import openstudio
import pandas as pd
from typing import Dict, List, Any

def validator(osm_model: openstudio.model.Model, spaces_data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Validates that the model and input data are ready for the task.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model object.
        spaces_data (List[Dict[str, Any]]): A list of dictionaries, where each
                                             dictionary represents a space and its data to be updated.
                                             Must contain a 'Name' or 'Handle' key.

    Returns:
        Dict[str, List[str]]: A dictionary with validation status and messages.
    """
    messages = []
    
    if not spaces_data:
        return {"status": "ERROR", "messages": ["ERROR: The input 'spaces_data' list is empty."]}

    # Check if all dicts have a required key (Name or Handle)
    if not all('Name' in d or 'Handle' in d for d in spaces_data):
        return {"status": "ERROR", "messages": ["ERROR: Each dictionary in 'spaces_data' must have a 'Name' or 'Handle' key."]}

    # Check that spaces from the data exist in the model
    missing_spaces = []
    for space_dict in spaces_data:
        space_name = space_dict.get('Name')
        if space_name and osm_model.getSpaceByName(space_name).isEmpty():
            missing_spaces.append(space_name)

    if missing_spaces:
        messages.append(f"WARNING: The following {len(missing_spaces)} spaces from your data were not found in the model and will be skipped: {missing_spaces[:5]}...")
    
    messages.append(f"OK: Ready to process {len(spaces_data)} data entries.")
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model, spaces_data: List[Dict[str, Any]]) -> openstudio.model.Model:
    """
    Updates geometric properties (Floor Area, Volume, Ceiling Height) for spaces
    based on a provided list of dictionaries.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model to modify.
        spaces_data (List[Dict[str, Any]]): The data to update.

    Returns:
        openstudio.model.Model: The modified OpenStudio model object.
    """
    print("INFO: Starting 'Set Space Data' task...")
    
    updated_count = 0
    for space_dict in spaces_data:
        space_name = space_dict.get('Name')
        if not space_name: continue # Skip if no name provided

        space_obj = osm_model.getSpaceByName(space_name)
        if space_obj.is_initialized():
            space = space_obj.get()
            
            # Update properties only if they exist in the dictionary and are different
            if 'Floor Area {m2}' in space_dict and space.floorArea() != space_dict['Floor Area {m2}']:
                space.setFloorArea(space_dict['Floor Area {m2}'])

            if 'Volume {m3}' in space_dict and space.volume() != space_dict['Volume {m3}']:
                space.setVolume(space_dict['Volume {m3}'])

            if 'Ceiling Height {m}' in space_dict and space.ceilingHeight() != space_dict['Ceiling Height {m}']:
                space.setCeilingHeight(space_dict['Ceiling Height {m}'])
            
            updated_count += 1
            
    print(f"INFO: Task finished. Data for {updated_count} spaces was processed.")
    return osm_model