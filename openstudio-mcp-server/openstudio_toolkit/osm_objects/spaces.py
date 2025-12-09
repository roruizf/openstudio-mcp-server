import openstudio
import pandas as pd


def get_space_object_as_dict(osm_model: openstudio.model.Model, space_handle: str = None, space_name: str = None) -> dict:
    """
    Retrieve a space from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_handle (str, optional): The handle of the space to retrieve.
    - space_name (str, optional): The name of the space to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified space.
    """

    if space_handle is not None and space_name is not None:
        raise ValueError(
            "Only one of 'space_handle' or 'space_name' should be provided.")
    if space_handle is None and space_name is None:
        raise ValueError(
            "Either 'space_handle' or 'space_name' must be provided.")

    # Find the space by handle or name
    if space_handle is not None:
        space_object = osm_model.getSpace(space_handle)
        if space_object.isNull():
            print(f"No space found with the handle: {space_handle}")
            return {}

    elif space_name is not None:
        space_object = osm_model.getSpaceByName(space_name)
        if space_object.isNull():
            print(f"No space found with the name: {space_name}")
            return {}

    target_space = space_object.get()

    # Define attributes to retrieve in a dictionary
    space_dict = {
        'Handle': str(target_space.handle()),
        'Name': target_space.name().get() if target_space.name().is_initialized() else None,
        'Space Type Name': target_space.spaceType().get().name().get() if target_space.spaceType().is_initialized() else None,
        'Default Construction Set Name': target_space.defaultConstructionSet().get().name().get() if target_space.defaultConstructionSet().is_initialized() else None,
        'Default Schedule Set Name': target_space.defaultScheduleSet().get().name().get() if target_space.defaultScheduleSet().is_initialized() else None,
        'Direction of Relative North {deg}': target_space.directionofRelativeNorth(),
        'X Origin {m}': target_space.xOrigin(),
        'Y Origin {m}': target_space.yOrigin(),
        'Z Origin {m}': target_space.zOrigin(),
        'Building Story Name': target_space.buildingStory().get().name().get() if target_space.buildingStory().is_initialized() else None,
        'Thermal Zone Name': target_space.thermalZone().get().name().get() if target_space.thermalZone().is_initialized() else None,
        'Part of Total Floor Area': target_space.partofTotalFloorArea(),
        'Design Specification Outdoor Air Object Name': target_space.designSpecificationOutdoorAir().get().name().get() if target_space.designSpecificationOutdoorAir().is_initialized() else None,
        'Building Unit Name': target_space.buildingUnit().get().name().get() if target_space.buildingUnit().is_initialized() else None,
        'Volume {m3}': target_space.volume(),
        'Ceiling Height {m}': target_space.ceilingHeight(),
        'Floor Area {m2}': target_space.floorArea()
    }

    return space_dict


def get_all_space_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all spaces from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getSpaces()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_space_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_space_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all spaces from the OpenStudio model using a specified method and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all spaces.
    """

    all_objects_dicts = get_all_space_objects_as_dicts(osm_model)

    # Create a DataFrame of all spaces.
    all_spaces_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_spaces_df = all_spaces_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_spaces_df.shape[0]} spaces")

    return all_spaces_df


def get_all_thermal_zones_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all thermal zones from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_objects_dicts = get_all_thermal_zones_objects_as_dicts(osm_model)

    # Create a DataFrame of all thermal zones.
    all_thermal_zones_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_thermal_zones_df = all_thermal_zones_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_thermal_zones_df.shape[0]} thermal zones")

    return all_thermal_zones_df


def update_space_object(osm_model, space_handle: str = None, space_name: str = None, attributes: dict = None):

    target_object_dict = get_space_object_as_dict(
        osm_model, space_handle, space_name)
