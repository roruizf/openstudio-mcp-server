# src/openstudio_toolkit/tasks/model_setup/rename_subsurfaces_based_on_parent_names.py

import openstudio
import pandas as pd
from typing import Dict, List, Tuple
from openstudio_toolkit.osm_objects import surfaces, subsurfaces

def _get_and_prepare_dataframes(osm_model: openstudio.model.Model) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Sub-task: Extracts and prepares the initial dataframes for surfaces and subsurfaces."""
    
    # Prepare Subsurfaces DataFrame
    subsurfaces_df = subsurfaces.get_all_subsurface_objects_as_dataframe(osm_model)
    subsurfaces_df = subsurfaces_df.rename(columns={'Handle': 'Sub Surface Handle', 'Name': 'Sub Surface Name'})
    subsurfaces_df = subsurfaces_df.sort_values(by='Sub Surface Handle', ascending=True).reset_index(drop=True)

    # Prepare Surfaces DataFrame
    surfaces_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    surfaces_df = surfaces_df.rename(columns={'Handle': 'Surface Handle', 'Name': 'Surface Name'})
    surfaces_df = surfaces_df.sort_values(by='Surface Name', ascending=True).reset_index(drop=True)

    return subsurfaces_df, surfaces_df

def _generate_and_deduplicate_names(subsurfaces_df: pd.DataFrame, surfaces_df: pd.DataFrame) -> pd.DataFrame:
    """Sub-task: Merges dataframes, generates new names, and ensures they are unique."""
    
    # Merge to link subsurfaces to their parent space
    merged_df = pd.merge(subsurfaces_df, surfaces_df, on='Surface Name', how='left')

    # Generate the new base name
    merged_df['New Sub Surface Name'] = merged_df['Surface Name'] + "_" + merged_df['Sub Surface Type']

    # --- De-duplication Logic ---
    # Separate unique and duplicate base names to process them
    duplicates_mask = merged_df.duplicated(subset=['New Sub Surface Name'], keep=False)
    unique_df = merged_df[~duplicates_mask]
    duplicate_df = merged_df[duplicates_mask]

    counter = {}
    
    # Process unique values to add a '_1' suffix
    for idx, row in unique_df.iterrows():
        value = row['New Sub Surface Name']
        new_value = f"{value}_1"
        merged_df.loc[idx, 'New Sub Surface Name'] = new_value
        counter[value] = 1

    # Process duplicate values to add incremental suffixes
    for idx, row in duplicate_df.iterrows():
        value = row['New Sub Surface Name']
        if value in counter:
            counter[value] += 1
        else:
            counter[value] = 1
        new_value = f"{value}_{counter[value]}"
        merged_df.loc[idx, 'New Sub Surface Name'] = new_value
        
    return merged_df

def _apply_names_to_model(osm_model: openstudio.model.Model, final_df: pd.DataFrame) -> None:
    """Sub-task: Applies the generated names back to the OpenStudio model objects."""
    for index, row in final_df.iterrows():
        subsurface = osm_model.getSubSurface(row['Sub Surface Handle']).get()
        new_name = row['New Sub Surface Name']
        if subsurface.nameString() != new_name:
            subsurface.setName(new_name)

# --- Main Task Functions ---

def validator(osm_model: openstudio.model.Model) -> Dict[str, List[str]]:
    """Validates that the model has subsurfaces to be renamed."""
    if len(osm_model.getSubSurfaces()) == 0:
        return {"status": "ERROR", "messages": ["ERROR: Model contains no subsurfaces to rename."]}
    
    messages = [f"OK: Found {len(osm_model.getSubSurfaces())} subsurfaces to process."]
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """Renames all subsurfaces based on their parent surface and space names."""
    print("INFO: Starting rename subsurfaces task...")
    
    # 1. Prepare Data
    subsurfaces_df, surfaces_df = _get_and_prepare_dataframes(osm_model)
    
    # 2. Generate and De-duplicate Names
    final_df = _generate_and_deduplicate_names(subsurfaces_df, surfaces_df)
    
    # 3. Apply Names to Model
    _apply_names_to_model(osm_model, final_df)
            
    print("INFO: Rename subsurfaces task finished successfully.")
    return osm_model