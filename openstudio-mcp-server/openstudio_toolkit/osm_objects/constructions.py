import openstudio
import pandas as pd
from typing import Dict, Optional

def get_all_construction_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Constructions from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about Constructions.
    """

    all_objects = osm_model.getConstructions()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_objects],
        'Name': [x.name().get() for x in all_objects],
        'Surface Rendering Name': [x.renderingColor().get().name().get() if not x.renderingColor().isNull() else None for x in all_objects], 
        }

    # Create a DataFrame of all thermal zones.
    all_objects_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_objects_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)
    
    # Get maximum number of Layers
    num_elements_max = 0
    for item in all_objects:
        num_elements = len(item.layers())
        if num_elements > num_elements_max:
            num_elements_max = num_elements
    
    for i in range(num_elements_max):
      all_objects_df[f'Layer {i+1}'] = None
    
    for index, row in all_objects_df.iterrows():
      # Add columns for each layer
      construction = osm_model.getConstructionByName(row['Name']).get()
      for i in range(len(construction.layers())):
        all_objects_df.loc[index, f'Layer {i+1}'] = construction.layers()[i].name().get()
       

    print(
        f"The OSM model contains {all_objects_df.shape[0]} constructions")

    return all_objects_df


def get_all_default_construction_set_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # Get all spaces in the OpenStudio model.
    all_default_construction_sets = osm_model.getDefaultConstructionSets()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_default_construction_sets],
                   'Name': [x.name().get() for x in all_default_construction_sets],
                   'Default Exterior Surface Constructions Name': [x.defaultExteriorSurfaceConstructions().get().name().get() if not x.defaultExteriorSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Interior Surface Constructions Name': [x.defaultInteriorSurfaceConstructions().get().name().get() if not x.defaultInteriorSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Ground Contact Surface Constructions Name': [x.defaultGroundContactSurfaceConstructions().get().name().get() if not x.defaultGroundContactSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Exterior SubSurface Constructions Name': [x.defaultExteriorSubSurfaceConstructions().get().name().get() if not x.defaultExteriorSubSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Interior SubSurface Constructions Name': [x.defaultInteriorSubSurfaceConstructions().get().name().get() if not x.defaultInteriorSubSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Interior Partition Construction Name': [x.interiorPartitionConstruction().get().name().get() if not x.interiorPartitionConstruction().isNull() else None for x in all_default_construction_sets],
                   'Space Shading Construction Name': [x.spaceShadingConstruction().get().name().get() if not x.spaceShadingConstruction().isNull() else None for x in all_default_construction_sets],
                   'Building Shading Construction Name': [x.buildingShadingConstruction().get().name().get() if not x.buildingShadingConstruction().isNull() else None for x in all_default_construction_sets],
                   'Site Shading Construction Name': [x.siteShadingConstruction().get().name().get() if not x.siteShadingConstruction().isNull() else None for x in all_default_construction_sets],
                   'Adiabatic Surface Construction Name': [x.adiabaticSurfaceConstruction().get().name().get() if not x.adiabaticSurfaceConstruction().isNull() else None for x in all_default_construction_sets]
                   }

    # Create a DataFrame of all spaces.
    all_default_construction_sets_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_default_construction_sets_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_default_construction_sets_df = all_default_construction_sets_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_default_construction_sets_df.shape[0]} default construction sets")

    return all_default_construction_sets_df


def get_all_default_surface_construction_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # Get all spaces in the OpenStudio model.
    all_default_surface_constructions = osm_model.getDefaultSurfaceConstructionss()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_default_surface_constructions],
                   'Name': [x.name().get() for x in all_default_surface_constructions],
                   'Floor Construction Name': [x.floorConstruction().get().name().get() if not x.floorConstruction().isNull() else None for x in all_default_surface_constructions],
                   'Wall Construction Name': [x.wallConstruction().get().name().get() if not x.wallConstruction().isNull() else None for x in all_default_surface_constructions],
                   'Roof Ceiling Construction Name': [x.roofCeilingConstruction().get().name().get() if not x.roofCeilingConstruction().isNull() else None for x in all_default_surface_constructions]
                   }

    # Create a DataFrame of all spaces.
    all_default_surface_constructions_df = pd.DataFrame(
        columns=object_attr.keys())
    for key in object_attr.keys():
        all_default_surface_constructions_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_default_surface_constructions_df = all_default_surface_constructions_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_default_surface_constructions_df.shape[0]} default surface constructions")

    return all_default_surface_constructions_df


def get_all_default_subsurface_construction_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # Get all spaces in the OpenStudio model.
    all_default_subsurface_constructions = osm_model.getDefaultSubSurfaceConstructionss()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_default_subsurface_constructions],
                   'Name': [x.name().get() for x in all_default_subsurface_constructions],
                   'Fixed Window Construction Name': [x.fixedWindowConstruction().get().name().get() if not x.fixedWindowConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Operable Window Construction Name': [x.operableWindowConstruction().get().name().get() if not x.operableWindowConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Door Construction Name': [x.doorConstruction().get().name().get() if not x.doorConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Glass Door Construction Name': [x.glassDoorConstruction().get().name().get() if not x.glassDoorConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Overhead Door Construction Name': [x.overheadDoorConstruction().get().name().get() if not x.overheadDoorConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Skylight Construction Name': [x.skylightConstruction().get().name().get() if not x.skylightConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Tubular Daylight Dome Construction Name': [x.tubularDaylightDomeConstruction().get().name().get() if not x.tubularDaylightDomeConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Tubular Daylight Diffuser Construction Name': [x.tubularDaylightDiffuserConstruction().get().name().get() if not x.tubularDaylightDiffuserConstruction().isNull() else None for x in all_default_subsurface_constructions]
                   }

    # Create a DataFrame of all spaces.
    all_default_subsurface_constructions_df = pd.DataFrame(
        columns=object_attr.keys())
    for key in object_attr.keys():
        all_default_subsurface_constructions_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_default_subsurface_constructions_df = all_default_subsurface_constructions_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_default_subsurface_constructions_df.shape[0]} default subsurface constructions")
    return all_default_subsurface_constructions_df


def get_all_default_construction_set_component_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:

    # Load required Data Frames
    all_default_construction_sets_df = get_all_default_construction_set_objects_as_dataframe(
        osm_model)
    all_default_surface_constructions_df = get_all_default_surface_construction_objects_as_dataframe(
        osm_model)
    all_default_subsurface_constructions_df = get_all_default_subsurface_construction_objects_as_dataframe(
        osm_model)

    # Define required dictionaries
    ext_surf_constr_dict = {'Exterior Surface Construction Walls': 'Wall Construction Name',
                            'Exterior Surface Construction Floors': 'Floor Construction Name',
                            'Exterior Surface Construction Roofs': 'Roof Ceiling Construction Name'
                            }
    int_surf_constr_dict = {
        'Interior Surface Construction Walls': 'Wall Construction Name',
        'Interior Surface Construction Floors': 'Floor Construction Name',
        'Interior Surface Construction Ceilings': 'Roof Ceiling Construction Name'
    }
    ground_surf_constr_dict = {
        'Ground Contact Surface Construction Walls': 'Wall Construction Name',
        'Ground Contact Surface Construction Floors': 'Floor Construction Name',
        'Ground Contact Surface Construction Ceilings': 'Roof Ceiling Construction Name'
    }
    ext_subsurf_constr_dict = {
        'Exterior SubSurface Construction Fixed Windows': 'Fixed Window Construction Name',
        'Exterior SubSurface Construction Operable Windows': 'Operable Window Construction Name',
        'Exterior SubSurface Construction Doors': 'Door Construction Name',
        'Exterior SubSurface Construction Glass Doors': 'Glass Door Construction Name',
        'Exterior SubSurface Construction Overhead Doors': 'Overhead Door Construction Name',
        'Exterior SubSurface Construction Skylights': 'Skylight Construction Name',
        'Exterior SubSurface Construction Tubular Daylight Domes': 'Tubular Daylight Dome Construction Name',
        'Exterior SubSurface Construction Tubular Daylight Diffusers': 'Tubular Daylight Diffuser Construction Name'
    }

    int_subsurf_constr_dict = {
        'Interior SubSurface Construction Fixed Windows': 'Fixed Window Construction Name',
        'Interior SubSurface Construction Operable Windows': 'Operable Window Construction Name',
        'Interior SubSurface Construction Doors': 'Door Construction Name'
    }

    all_default_construction_sets_components_df = all_default_construction_sets_df[[
        'Handle', 'Name']].copy()
    # Default Exterior Surface Constructions
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in ext_surf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Exterior Surface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_surface_constructions_df.loc[
                all_default_surface_constructions_df['Name'] == name, value].values[0]
    # Default Interior Surface Constructions
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in int_surf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Interior Surface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_surface_constructions_df.loc[
                all_default_surface_constructions_df['Name'] == name, value].values[0]

    # Default Ground Contact Surface Constructions
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in ground_surf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Ground Contact Surface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_surface_constructions_df.loc[
                all_default_surface_constructions_df['Name'] == name, value].values[0]

    # Default Exterior SubSurface Constructions Name
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in ext_subsurf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Exterior SubSurface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_subsurface_constructions_df.loc[
                all_default_subsurface_constructions_df['Name'] == name, value].values[0]

    # Default Interior SubSurface Constructions Name
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in int_subsurf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Interior SubSurface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_subsurface_constructions_df.loc[
                all_default_subsurface_constructions_df['Name'] == name, value].values[0]

    # Other Constructions
    cols = ['Space Shading Construction Name', 'Building Shading Construction Name',
            'Site Shading Construction Name', 'Interior Partition Construction Name', 'Adiabatic Surface Construction Name']
    all_default_construction_sets_components_df[cols] = all_default_construction_sets_df[cols].copy(
    )
    return all_default_construction_sets_components_df

def create_new_construction_set_from_dict(osm_model: openstudio.model.Model, construction_set_name: str, construction_set_dict: Dict[str, Optional[Dict[str, str]]]) -> openstudio.model.Model:
    """
    Creates a new default construction set in the OpenStudio model based on the provided construction set dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - construction_set_name (str): The name of the new construction set.
    - construction_set_dict (Dict[str, Optional[Dict[str, str]]]): A dictionary containing the construction set details, where the keys are the construction types and the values are dictionaries with the construction names.

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object with the new construction set.
    """
    # Create a default construction set
    default_construction_set = openstudio.model.DefaultConstructionSet(osm_model)
    default_construction_set.setName(construction_set_name)

    all_default_construction_sets_df = get_all_default_construction_set_objects_as_dataframe(osm_model)
    default_construction_set_df = all_default_construction_sets_df.loc[all_default_construction_sets_df['Name'].isin([construction_set_name])].reset_index(drop=True)
    default_construction_set_attr = default_construction_set_df.drop(['Handle', 'Name'], axis=1).columns.to_list()

    # Get Default Surface Constructions
    default_surface_constructions_types = [item.replace('Default', '').replace('Name', '').strip() for item in default_construction_set_attr if 'Surface Constructions' in item and 'SubSurface Constructions' not in item]

    for surface_construction_type in default_surface_constructions_types:
        if construction_set_dict[surface_construction_type] is not None:
            default_surface_construction = openstudio.model.DefaultSurfaceConstructions(osm_model)
            default_surface_construction.setName(construction_set_name + " " + surface_construction_type.replace('Name', '').strip())

            all_default_surface_constructions_df = get_all_default_surface_construction_objects_as_dataframe(osm_model)
            default_surface_constructions_df = all_default_surface_constructions_df.loc[all_default_surface_constructions_df['Name'].isin([default_surface_construction.nameString()])].reset_index(drop=True)

            default_constructions_attr = default_surface_constructions_df.drop(['Handle', 'Name'], axis=1).columns.to_list()
            default_constructions_types = [item.replace('Name', '').replace('Construction', '').strip() for item in default_constructions_attr if 'Construction' in item]

            for construction_type in default_constructions_types:      
                if construction_set_dict[surface_construction_type][construction_type] is not None:
                    default_construction = openstudio.model.Construction(osm_model)
                    default_construction_name = surface_construction_type.replace('Surface Constructions', '').strip() + " " + construction_type + ":" + construction_set_name
                    default_construction.setName(default_construction_name)

                    # Set Default Constructions to Set Surface Constructions
                    if 'Floor' in default_construction.nameString():
                        default_surface_construction.setFloorConstruction(default_construction)
                    elif 'Wall' in default_construction.nameString():
                        default_surface_construction.setWallConstruction(default_construction)
                    elif 'Roof Ceiling' in default_construction.nameString():
                        default_surface_construction.setRoofCeilingConstruction(default_construction)

            # Set Surface Constructions to Default Construction Set
            if 'Exterior Surface Constructions' in default_surface_construction.nameString():
                default_construction_set.setDefaultExteriorSurfaceConstructions(default_surface_construction)
            elif 'Interior Surface Constructions' in default_surface_construction.nameString():
                default_construction_set.setDefaultInteriorSurfaceConstructions(default_surface_construction)
            elif 'Ground Contact Surface Constructions' in default_surface_construction.nameString():
                default_construction_set.setDefaultGroundContactSurfaceConstructions(default_surface_construction)

    # Get Default SubSurface Constructions
    default_subsurface_constructions_types = [item.replace('Default', '').replace('Name', '').strip() for item in default_construction_set_attr if 'SubSurface Constructions Name' in item]

    for subsurface_construction_type in default_subsurface_constructions_types:
        if construction_set_dict[subsurface_construction_type] is not None:
            default_subsurface_construction = openstudio.model.DefaultSubSurfaceConstructions(osm_model)
            default_subsurface_construction.setName(construction_set_name + " " + subsurface_construction_type.replace('Name', '').strip())

            all_default_subsurface_constructions_df = get_all_default_subsurface_construction_objects_as_dataframe(osm_model)
            default_subsurface_constructions_df = all_default_subsurface_constructions_df.loc[all_default_subsurface_constructions_df['Name'].isin([default_subsurface_construction.nameString()])].reset_index(drop=True)

            default_constructions_attr = default_subsurface_constructions_df.drop(['Handle', 'Name'], axis=1).columns.to_list()
            default_constructions_types = [item.replace('Name', '').replace('Construction', '').strip() for item in default_constructions_attr if 'Construction' in item]

            for construction_type in default_constructions_types:      
                if construction_set_dict[subsurface_construction_type][construction_type] is not None:
                    default_construction = openstudio.model.Construction(osm_model)
                    default_construction_name = subsurface_construction_type.replace('SubSurface Constructions', '').strip() + " " + construction_type + ":" + construction_set_name
                    default_construction.setName(default_construction_name)

                    all_default_constructions_df = get_all_construction_objects_as_dataframe(osm_model)
                    default_constructions_df = all_default_constructions_df.loc[all_default_constructions_df['Name'].isin([default_construction.nameString()])].reset_index(drop=True)

                    # Set Default Constructions to Set Surface Constructions        
                    if 'Fixed Window' in default_construction.nameString():
                        default_subsurface_construction.setFixedWindowConstruction(default_construction)
                    elif 'Operable Window' in default_construction.nameString():
                        default_subsurface_construction.setOperableWindowConstruction(default_construction)
                    elif 'Glass Door' in default_construction.nameString():
                        if 'Exterior SubSurface Constructions' in default_subsurface_construction.nameString():
                            default_subsurface_construction.setGlassDoorConstruction(default_construction)
                    elif 'Overhead Door' in default_construction.nameString():
                        if 'Exterior SubSurface Constructions' in default_subsurface_construction.nameString():
                            default_subsurface_construction.setOverheadDoorConstruction(default_construction)
                    elif 'Door' in default_construction.nameString():
                        default_subsurface_construction.setDoorConstruction(default_construction)
                    elif 'Skylight' in default_construction.nameString():
                        if 'Exterior SubSurface Constructions' in default_subsurface_construction.nameString():
                            default_subsurface_construction.setSkylightConstruction(default_construction)
                    elif 'Tubular Daylight Dome' in default_construction.nameString():
                        if 'Exterior SubSurface Constructions' in default_subsurface_construction.nameString():
                            default_subsurface_construction.setTubularDaylightDomeConstruction(default_construction)
                    elif 'Tubular Daylight Diffuser' in default_construction.nameString():
                        if 'Exterior SubSurface Constructions' in default_subsurface_construction.nameString():
                            default_subsurface_construction.setTubularDaylightDiffuserConstruction(default_construction)

            # Set Surface Constructions to Default Construction Set
            if 'Exterior SubSurface Constructions' in default_subsurface_construction.nameString():
                default_construction_set.setDefaultExteriorSubSurfaceConstructions(default_subsurface_construction)
            elif 'Interior SubSurface Constructions' in default_subsurface_construction.nameString():
                default_construction_set.setDefaultInteriorSubSurfaceConstructions(default_subsurface_construction)

    # Interior Partition Construction Name
    # Space Shading Construction Name
    # Building Shading Construction Name
    # Site Shading Construction Name
    # Adiabatic Surface Construction Name

    return osm_model
