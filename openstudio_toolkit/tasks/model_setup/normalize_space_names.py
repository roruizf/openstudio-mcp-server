# src/openstudio_toolkit/tasks/model_setup/normalize_space_names.py

import openstudio
import re
from typing import Dict, List

def _is_normalized(space_name: str) -> bool:
    """Checks if a space name is already normalized (contains no spaces or underscores)."""
    return " " not in space_name and "_" not in space_name

def validator(osm_model: openstudio.model.Model) -> Dict[str, List[str]]:
    """
    Validates that the model has spaces and checks if they need normalization.
    """
    spaces = osm_model.getSpaces()
    if len(spaces) == 0:
        return {"status": "ERROR", "messages": ["ERROR: Model contains no spaces to normalize."]}

    # Check if any space name actually needs normalization
    needs_normalization = any(not _is_normalized(s.nameString()) for s in spaces)

    if not needs_normalization:
        messages = [f"OK: Found {len(spaces)} spaces.", "INFO: All space names are already normalized. Nothing to do."]
        return {"status": "SKIP", "messages": messages}
    
    messages = [f"OK: Found {len(spaces)} spaces that require normalization."]
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """
    Normalizes all space names in the model by replacing spaces and underscores
    with hyphens and removing trailing/leading whitespace.
    """
    print("INFO: Starting normalize space names task...")
    
    spaces_renamed_count = 0
    for space in osm_model.getSpaces():
        original_name = space.nameString()
        # Replace spaces and underscores with hyphens, and strip whitespace
        normalized_name = original_name.replace(" ", "-").replace("_", "-").strip()
        
        if original_name != normalized_name:
            space.setName(normalized_name)
            spaces_renamed_count += 1
            
    print(f"INFO: Task finished. {spaces_renamed_count} space names were normalized.")
    return osm_model