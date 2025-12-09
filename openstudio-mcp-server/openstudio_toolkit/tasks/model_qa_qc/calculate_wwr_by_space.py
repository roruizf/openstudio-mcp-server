# src/openstudio_toolkit/tasks/model_qa_qc/calculate_wwr_by_space.py

import openstudio
import pandas as pd
from typing import Dict, List
from openstudio_toolkit.osm_objects import surfaces, subsurfaces

def validator(osm_model: openstudio.model.Model) -> Dict[str, List[str]]:
    """
    Diagnoses if the model has the necessary components to calculate WWR.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model object to validate.

    Returns:
        Dict[str, List[str]]: A dictionary containing the validation status
        ('READY' or 'ERROR') and a list of human-readable messages.
    """
    messages = []
    surface_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    if surface_df.empty:
        messages.append("ERROR: Model does not contain any surfaces.")
        return {"status": "ERROR", "messages": messages}

    walls_df = surface_df[
        (surface_df['Surface Type'] == 'Wall') & 
        (surface_df['Outside Boundary Condition'] == 'Outdoors')
    ]

    if walls_df.empty:
        messages.append("ERROR: Model contains no outdoor-facing 'Wall' surfaces.")
        return {"status": "ERROR", "messages": messages}

    messages.append(f"OK: Found {len(walls_df)} outdoor-facing walls.")
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Calculates the Window-to-Wall Ratio (WWR) for each space.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model object to process.

    Returns:
        pd.DataFrame: A DataFrame with WWR calculations per space.
    """
    print("INFO: Starting WWR calculation task...")

    all_surfaces_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    all_subsurfaces_df = subsurfaces.get_all_subsurface_objects_as_dataframe(osm_model)

    all_surfaces_df['Surface Gross Area'] = all_surfaces_df['Handle'].apply(lambda handle: osm_model.getSurface(handle).get().grossArea())
    all_subsurfaces_df['Sub Surface Gross Area'] = all_subsurfaces_df['Handle'].apply(lambda handle: osm_model.getSubSurface(handle).get().grossArea())

    subsurface_space_map = {
        s.nameString(): s.space().get().nameString() 
        for s in osm_model.getSurfaces() if s.space().is_initialized()
    }
    all_subsurfaces_df['Space Name'] = all_subsurfaces_df['Surface Name'].map(subsurface_space_map)

    walls_df = all_surfaces_df[(all_surfaces_df['Surface Type'] == 'Wall') & (all_surfaces_df['Outside Boundary Condition'] == 'Outdoors')]
    walls_by_space = walls_df.groupby('Space Name')['Surface Gross Area'].sum().reset_index()

    window_types = ('FixedWindow', 'OperableWindow', 'GlassDoor')
    windows_df = all_subsurfaces_df[all_subsurfaces_df['Sub Surface Type'].isin(window_types)]
    windows_by_space = windows_df.groupby('Space Name')['Sub Surface Gross Area'].sum().reset_index()

    wwr_df = pd.merge(walls_by_space, windows_by_space, on='Space Name', how='left').fillna(0)
    wwr_df['WWR'] = (wwr_df['Sub Surface Gross Area'] / wwr_df['Surface Gross Area']).fillna(0)

    print("INFO: WWR calculation task finished successfully.")
    return wwr_df