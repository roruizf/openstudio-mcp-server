import openstudio
import pandas as pd

def get_surface_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a surface object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the surface to retrieve.
    - name (str, optional): The name of the surface to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified surface.
    """
    # Define the methods to retrieve surfaces by handle and name
    get_surface_by_handle = osm_model.getSurface
    get_surface_by_name = osm_model.getSurfaceByName

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the surface by handle or name
    if handle is not None:
        surface_obj = get_surface_by_handle(handle)
        if surface_obj.isNull():
            print(f"No surface found with the handle: {handle}")
            return {}
    elif name is not None:
        surface_obj = get_surface_by_name(name)
        if surface_obj.isNull():
            print(f"No surface found with the name: {name}")
            return {}

    target_surface = surface_obj.get()

    # Define attributes to retrieve
    surface_dict = {
        'Handle': str(target_surface.handle()),
        'Name': target_surface.name().get() if target_surface.name().is_initialized() else None,
        'Surface Type': target_surface.surfaceType(),
        'Construction Name': target_surface.construction().get().name().get() if not target_surface.construction().isNull() else None,        
        'Space Name': target_surface.space().get().name().get(),
        'Outside Boundary Condition': target_surface.outsideBoundaryCondition(),
        'Outside Boundary Condition Object': target_surface.adjacentSurface().get().name().get() if not target_surface.adjacentSurface().isNull() else None,
        'Sun Exposure': target_surface.sunExposure(),
        'Wind Exposure': target_surface.windExposure(),
        'View Factor to Ground': None,
        'Number of Vertices': None
    }

    return surface_dict


def get_all_surface_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all surface objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a surface object.
    """

    # Get all surface objects in the OpenStudio model.
    all_surfaces = osm_model.getSurfaces()

    all_surfaces_dicts = []

    for target_surface in all_surfaces:
        object_handle = str(target_surface.handle())
        object_dict = get_surface_object_as_dict(osm_model, handle=object_handle)
        all_surfaces_dicts.append(object_dict)

    return all_surfaces_dicts

def get_all_surface_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:

    # Get all surfaces in the OpenStudio model.
    all_surfaces = osm_model.getSurfaces()
    # Define attributtes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_surfaces],
        'Name': [x.name().get() for x in all_surfaces],
        'Surface Type': [x.surfaceType() for x in all_surfaces],
        'Construction Name': [x.construction().get().name().get() if not x.construction().isNull() else None for x in all_surfaces],
        'Space Name': [x.space().get().name().get()
                       for x in all_surfaces],
        'Outside Boundary Condition': [x.outsideBoundaryCondition() for x in all_surfaces],
        'Outside Boundary Condition Object': [x.adjacentSurface().get().name(
        ).get() if not x.adjacentSurface().isNull() else None for x in all_surfaces],
        'Sun Exposure': [x.sunExposure() for x in all_surfaces],
        'Wind Exposure': [x.windExposure() for x in all_surfaces],
        'View Factor to Ground': None,
        'Number of Vertices': None
        # 'X,Y,Z Vertex 1 {m}': None,
        # 'X,Y,Z Vertex 2 {m}': None,
        # 'X,Y,Z Vertex 3 {m}': None,
        # 'X,Y,Z Vertex 4 {m}': None,
        # 'X,Y,Z Vertex 5 {m}': None,
        # 'X,Y,Z Vertex 6 {m}': None
    }
    # Create a DataFrame of all spaces.
    all_surfaces_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_surfaces_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the SpaceName column and reset indexes
    all_surfaces_df = all_surfaces_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_surfaces_df.shape[0]} surfaces")

    return all_surfaces_df
