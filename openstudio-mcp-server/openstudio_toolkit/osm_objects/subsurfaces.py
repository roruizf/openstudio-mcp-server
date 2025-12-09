import openstudio
import pandas as pd

def get_subsurface_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a subsurface object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the subsurface to retrieve.
    - name (str, optional): The name of the subsurface to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified subsurface.
    """
    # Define the methods to retrieve subsurfaces by handle and name
    get_subsurface_by_handle = osm_model.getSubSurface
    get_subsurface_by_name = osm_model.getSubSurfaceByName

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the subsurface by handle or name
    if handle is not None:
        subsurface_obj = get_subsurface_by_handle(handle)
        if subsurface_obj.isNull():
            print(f"No subsurface found with the handle: {handle}")
            return {}
    elif name is not None:
        subsurface_obj = get_subsurface_by_name(name)
        if subsurface_obj.isNull():
            print(f"No subsurface found with the name: {name}")
            return {}

    target_subsurface = subsurface_obj.get()

    # Define attributes to retrieve
    subsurface_dict = {
        'Handle': str(target_subsurface.handle()),
        'Name': target_subsurface.name().get() if target_subsurface.name().is_initialized() else None,
        'Sub Surface Type': target_subsurface.subSurfaceType(),
        'Construction Name': target_subsurface.construction().get().name().get() if not target_subsurface.construction().isNull() else None,
        'Surface Name': target_subsurface.parent().get().name().get(),
        'Outside Boundary Condition Object': target_subsurface.outsideBoundaryCondition(),
        'View Factor to Ground': None,
        'Frame and Divider Name': target_subsurface.windowPropertyFrameAndDivider().get().name().get() if not target_subsurface.windowPropertyFrameAndDivider().isNull() else None,
        'Multiplier': None,
        'Number of Vertices': None
    }

    return subsurface_dict

def get_all_subsurface_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all subsurface objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a subsurface object.
    """

    # Get all subsurface objects in the OpenStudio model.
    all_subsurfaces = osm_model.getSubSurfaces()

    all_subsurfaces_dicts = []

    for target_subsurface in all_subsurfaces:
        object_handle = str(target_subsurface.handle())
        object_dict = get_subsurface_object_as_dict(osm_model, handle=object_handle)
        all_subsurfaces_dicts.append(object_dict)

    return all_subsurfaces_dicts

def get_all_subsurface_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all subsurfaces from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all subsurfaces.
    """

    # Get all subsurfaces in the OpenStudio model.
    all_subsurfaces = osm_model.getSubSurfaces()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_subsurfaces],
        'Name': [x.nameString() for x in all_subsurfaces],
        'Sub Surface Type': [x.subSurfaceType() for x in all_subsurfaces],
        'Construction Name': [x.construction().get().name().get() if not x.construction().isNull() else None for x in all_subsurfaces],
        'Surface Name': [x.parent().get().name().get() for x in all_subsurfaces],
        'Outside Boundary Condition Object': [x.outsideBoundaryCondition() for x in all_subsurfaces],
        'View Factor to Ground': None,
        'Frame and Divider Name': [x.windowPropertyFrameAndDivider().get().name().get() if not x.windowPropertyFrameAndDivider().isNull() else None for x in all_subsurfaces],
        'Multiplier': None,
        'Number of Vertices': None
        # 'X,Y,Z Vertex 1 {m}': None,
        # 'X,Y,Z Vertex 2 {m}': None,
        # 'X,Y,Z Vertex 3 {m}': None,
        # 'X,Y,Z Vertex 4 {m}': None
    }

    # Create a DataFrame of all spaces.
    all_subsurfaces_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_subsurfaces_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_subsurfaces_df = all_subsurfaces_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_subsurfaces_df.shape[0]} sub-surfaces")
    return all_subsurfaces_df
