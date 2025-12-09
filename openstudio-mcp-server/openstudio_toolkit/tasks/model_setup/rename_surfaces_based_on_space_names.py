# src/openstudio_toolkit/tasks/model_setup/rename_surfaces_based_on_space_names.py

import openstudio
import pandas as pd
from typing import Dict, List
from openstudio_toolkit.osm_objects import surfaces

def _generate_new_surface_names(df: pd.DataFrame) -> pd.Series:
    """Sub-task: Generates the base names for surfaces."""
    
    # Create a map of surface names to their parent space names
    surface_to_space_map = df.set_index('Surface Name')['Space Name'].to_dict()

    # Case 1: Boundary condition is an object (adjacent surface)
    mask_adjacent = df['Outside Boundary Condition Object'].notnull()
    df.loc[mask_adjacent, 'New Surface Name'] = (
        df['Space Name'] + "_" +
        df['Surface Type'] + "_" +
        df['Outside Boundary Condition Object'].map(surface_to_space_map)
    )

    # Case 2: Boundary condition is a simple type (e.g., Outdoors)
    mask_simple = df['Outside Boundary Condition Object'].isnull()
    df.loc[mask_simple, 'New Surface Name'] = (
        df['Space Name'] + "_" +
        df['Surface Type'] + "_" +
        df['Outside Boundary Condition']
    )
    
    return df['New Surface Name']

def _deduplicate_names(names: pd.Series) -> pd.Series:
    """Sub-task: Appends suffixes to duplicate names to make them unique."""
    counts = {}
    new_names = []
    for name in names:
        if name in counts:
            counts[name] += 1
            new_names.append(f"{name}_{counts[name]}")
        else:
            counts[name] = 1
            new_names.append(f"{name}_1")
    return pd.Series(new_names, index=names.index)

# --- Main Task Functions ---

def validator(osm_model: openstudio.model.Model) -> Dict[str, List[str]]:
    """Validates that the model has surfaces to be renamed."""
    if len(osm_model.getSurfaces()) == 0:
        return {"status": "ERROR", "messages": ["ERROR: Model contains no surfaces to rename."]}
    
    messages = [f"OK: Found {len(osm_model.getSurfaces())} surfaces to process."]
    # Add a 'SKIP' check here in the future if desired
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """Renames all surfaces based on their space and boundary condition."""
    print("INFO: Starting rename surfaces task...")
    
    surfaces_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    surfaces_df = surfaces_df.rename(columns={'Handle': 'Surface Handle', 'Name': 'Surface Name'})

    # 1. Generate base names
    base_names = _generate_new_surface_names(surfaces_df)
    
    # 2. De-duplicate names
    final_names = _deduplicate_names(base_names)
    surfaces_df['New Surface Name'] = final_names

    # 3. Apply changes to the model
    for index, row in surfaces_df.iterrows():
        surface = osm_model.getSurface(row['Surface Handle']).get()
        new_name = row['New Surface Name']
        if surface.nameString() != new_name:
            surface.setName(new_name)
            
    print("INFO: Rename surfaces task finished successfully.")
    return osm_model