import openstudio
import pandas as pd

# --------------------------------------------------
#  ***** OS:Exterior:FuelEquipment:Definition ******
# --------------------------------------------------


def get_exterior_fuel_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Exterior:FuelEquipment:Definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getExteriorFuelEquipmentDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getExteriorFuelEquipmentDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle':  str(target_object.handle()), 
                   'Name': target_object.nameString(), 
                   'Design Level {W}': target_object.designLevel()}

    return object_dict

def get_all_exterior_fuel_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Exterior:FuelEquipment:Definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getExteriorFuelEquipmentDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_exterior_fuel_equipment_definition_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_exterior_fuel_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all exterior fuel equipment definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all exterior fuel equipment definition objects.
    """

    all_objects_dicts = get_all_exterior_fuel_equipment_definition_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Design Level {W}']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all exterior fuel equipment definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} exterior fuel equipment definition objects.")

    return all_objects_df


# --------------------------------------------------
#  ***** OS:Exterior:WaterEquipment:Definition *****
# --------------------------------------------------


def get_exterior_water_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Exterior:WaterEquipment:Definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getExteriorWaterEquipmentDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getExteriorWaterEquipmentDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle':  str(target_object.handle()), 
                   'Name': target_object.nameString(), 
                   'Design Level {m3/s}': target_object.designLevel()}

    return object_dict

def get_all_exterior_water_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Exterior:WaterEquipment:Definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getExteriorWaterEquipmentDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_exterior_water_equipment_definition_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_exterior_water_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all exterior water equipment definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all exterior water equipment definition objects.
    """

    all_objects_dicts = get_all_exterior_water_equipment_definition_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Design Level {m3/s}']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all exterior water equipment definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} exterior water equipment definition objects.")

    return all_objects_df


# --------------------------------------------------
#  ***** OS:Exterior:Lights:Definition *************
# --------------------------------------------------


def get_exterior_lights_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Exterior:Lights:Definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getExteriorLightsDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getExteriorLightsDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle':  str(target_object.handle()), 
                   'Name': target_object.nameString(), 
                   'Design Level {W}': target_object.designLevel()}

    return object_dict

def get_all_exterior_lights_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Exterior:Lights:Definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getExteriorLightsDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_exterior_lights_definition_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_exterior_lights_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all exterior lights definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all exterior lights definition objects.
    """

    all_objects_dicts = get_all_exterior_lights_definition_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Design Level {W}']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all exterior lights definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} exterior lights definition objects.")

    return all_objects_df