import openstudio
import pandas as pd
import numpy as np

def get_standard_opaque_material_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a standard opaque material from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the standard opaque material to retrieve.
    - name (str, optional): The name of the standard opaque material to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified standard opaque material.
    """

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the standard opaque material by handle or name
    if handle is not None:
        osm_object = osm_model.getStandardOpaqueMaterial(handle)
        if osm_object is None:
            print(
                f"No standard opaque material found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getStandardOpaqueMaterialByName(name)
        if not osm_object:
            print(
                f"No standard opaque material found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Roughness': target_object.roughness(),
        'Thickness {m}': target_object.thickness(),
        'Conductivity {W/m-K}': target_object.thermalConductivity(),
        'Density {kg/m3}': target_object.density(),
        'Specific Heat {J/kg-K}': target_object.specificHeat(),
        'Thermal Absorptance': target_object.thermalAbsorptance(),
        'Solar Absorptance': target_object.solarAbsorptance(),
        'Visible Absorptance': target_object.visibleAbsorptance(),
        }

    return object_dict

def get_all_standard_opaque_material_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all standard opaque materials from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a standard opaque material.
    """

    # Get all standard opaque materials in the OpenStudio model.
    all_objects = osm_model.getStandardOpaqueMaterials()

    all_objects_dicts = []

    for target_object in all_objects:
        handle = str(target_object.handle())
        object_dict = get_standard_opaque_material_object_as_dict(osm_model, handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_standard_opaque_material_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all standard opaque materials from the OpenStudio model using a specified method and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all standard opaque materials.
    """

    all_objects_dicts = get_all_standard_opaque_material_objects_as_dicts(osm_model)

    # Create a DataFrame of all standard opaque materials.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} standard opaque materials")

    return all_objects_df

# --------------------------------------------------
#  ***** OS:Material:NoMass ************************
# --------------------------------------------------

def get_massless_opaque_material_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Material:NoMass object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to get.
    - name (str, optional): The name of the object to get.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the massless opaque material by handle or name
    if handle is not None:
        osm_object = osm_model.getMasslessOpaqueMaterial(handle)
        if osm_object is None:
            print(
                f"No massless opaque material found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getMasslessOpaqueMaterialByName(name)
        if not osm_object:
            print(
                f"No massless opaque material found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Roughness': target_object.roughness(),
        'Thermal Resistance {m2-K/W}': target_object.thermalResistance(),
        'Thermal Absorptance': target_object.thermalAbsorptance().get() if target_object.thermalAbsorptance().is_initialized() else None,
        'Solar Absorptance': target_object.solarAbsorptance().get() if target_object.solarAbsorptance().is_initialized() else None,
        'Visible Absorptance': target_object.visibleAbsorptance().get() if target_object.visibleAbsorptance().is_initialized() else None
    }

    return object_dict

def get_all_massless_opaque_material_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Material:NoMass objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a massless opaque material.
    """

    # Get all massless opaque materials in the OpenStudio model.
    all_objects = osm_model.getMasslessOpaqueMaterials()

    all_objects_dicts = []

    for target_object in all_objects:
        handle = str(target_object.handle())
        object_dict = get_massless_opaque_material_object_as_dict(osm_model, handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_massless_opaque_material_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all material no mass objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all material no mass objects.
    """

    all_objects_dicts = get_all_massless_opaque_material_objects_as_dicts(osm_model)

    # Create a DataFrame of all massless opaque materials.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} massless opaque materials")

    return all_objects_df

# --------------------------------------------------


def get_all_opaque_material_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all opaque material objects from an OpenStudio model as a DataFrame.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model to extract materials from.

    Returns:
        pd.DataFrame: DataFrame containing all opaque materials with their properties.
    """
    # Get all standard opaque materials and massless opaque materials
    all_standard_opaque_materials = osm_model.getStandardOpaqueMaterials()
    all_standard_opaque_materials_df = get_all_standard_opaque_material_objects_as_dataframe(osm_model)
    get_all_massless_opaque_materials_df = get_all_massless_opaque_material_objects_as_dataframe(osm_model)

    # Add 'Material Type' column to each DataFrame
    all_standard_opaque_materials_df['Material Type'] = 'Standard'
    get_all_massless_opaque_materials_df['Material Type'] = 'NoMass'

    # Calculate Thermal Resistance {m2-K/W}
    all_standard_opaque_materials_df['Thermal Resistance {m2-K/W}'] = all_standard_opaque_materials_df['Thickness {m}'] / all_standard_opaque_materials_df['Conductivity {W/m-K}']

    # Concatenate vertically
    all_opaque_materials_df = pd.concat(
        [all_standard_opaque_materials_df, get_all_massless_opaque_materials_df],
        ignore_index=True,
        sort=False
    )

    # Move 'Material Type' to the third position (index 2)
    cols = list(all_opaque_materials_df.columns)
    cols.remove('Material Type')  # Remove from current position
    cols.insert(1, 'Material Type')  # Insert at position 2 (third position)
    all_opaque_materials_df = all_opaque_materials_df[cols]

    # Replace NaN with None if desired
    all_opaque_materials_df = all_opaque_materials_df.replace({np.nan: None})

    return all_opaque_materials_df
