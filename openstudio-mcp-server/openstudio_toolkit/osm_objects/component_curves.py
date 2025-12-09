import openstudio
import pandas as pd

# --------------------------------------------------
#  ***** OS:Curve:Cubic ****************************
# --------------------------------------------------


def get_curve_cubic_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Curve:Cubic object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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
        osm_object = osm_model.getCurveCubic(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getCurveCubicByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle': str(target_object.handle()), 
                   'Name': target_object.nameString(), 
                   'Coefficient1 Constant': target_object.coefficient1Constant(), 
                   'Coefficient2 x': target_object.coefficient2x(), 
                   'Coefficient3 x**2': target_object.coefficient3xPOW2(), 
                   'Coefficient4 x**3': target_object.coefficient4xPOW3(), 
                   'Minimum Value of x': target_object.minimumValueofx(), 
                   'Maximum Value of x': target_object.maximumValueofx()}

    return object_dict

def get_all_curve_cubic_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Curve:Cubic objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a curve cubic object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getCurveCubics()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_curve_cubic_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_curve_cubic_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all curve cubic objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all curve cubic objects.
    """

    all_objects_dicts = get_all_curve_cubic_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Coefficient1 Constant', 'Coefficient2 x', 'Coefficient3 x**2', 'Coefficient4 x**3', 'Minimum Value of x', 'Maximum Value of x']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all curve cubic objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} curve cubic objects.")

    return all_objects_df


def get_all_quadratic_curves_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Quadratic Curves from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all spaces.
    """

    # Get all spaces in the OpenStudio model.
    all_quadratic_curves = osm_model.getCurveQuadratics()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_quadratic_curves],
        'Name': [x.name().get() for x in all_quadratic_curves],
        'Coefficient1 Constant': [x.coefficient1Constant() for x in all_quadratic_curves],
        'Coefficient2 x': [x.coefficient2x() for x in all_quadratic_curves],
        'Coefficient3 x**2': [x.coefficient3xPOW2() for x in all_quadratic_curves],  
        'Minimum Value of x': [x.minimumValueofx() for x in all_quadratic_curves],
        'Maximum Value of x': [x.maximumValueofx() for x in all_quadratic_curves]
    }

    # Create a DataFrame of all spaces.
    all_quadratic_curves_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_quadratic_curves_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_quadratic_curves_df = all_quadratic_curves_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_quadratic_curves_df.shape[0]} quadratic curves")

    return all_quadratic_curves_df

# --------------------------------------------------
#  ***** OS:Curve:Biquadratic **********************
# --------------------------------------------------

def get_curve_biquadratic_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Curve:Biquadratic object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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
        osm_object = osm_model.getCurveBiquadratic(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getCurveBiquadraticByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get(),
        'Coefficient1 Constant': target_object.coefficient1Constant(),
        'Coefficient2 x': target_object.coefficient2x(),
        'Coefficient3 x**2': target_object.coefficient3xPOW2(),  
        'Coefficient4 y': target_object.coefficient4y(),  
        'Coefficient5 y**2': target_object.coefficient5yPOW2(),  
        'Coefficient6 x*y': target_object.coefficient6xTIMESY(),  
        'Minimum Value of x': target_object.minimumValueofx(),
        'Maximum Value of x': target_object.maximumValueofx(),
        'Minimum Value of y': target_object.minimumValueofy(),
        'Maximum Value of y': target_object.maximumValueofy()
    }

    return object_dict

def get_all_curve_biquadratic_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Curve:Biquadratic objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a curve biquadratic object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getCurveBiquadratics()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_curve_biquadratic_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_curve_biquadratic_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all curve biquadratic objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all curve biquadratic objects.
    """

    all_objects_dicts = get_all_curve_biquadratic_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Coefficient1 Constant', 'Coefficient2 x', 'Coefficient3 x**2', 'Coefficient4 y', 'Coefficient5 y**2', 'Coefficient6 x*y', 'Minimum Value of x', 'Maximum Value of x', 'Minimum Value of y', 'Maximum Value of y']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all curve biquadratic objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} curve biquadratic objects.")

    return all_objects_df

# --------------------------------------------------
#  ***** OS:Curve:Exponent *************************
# --------------------------------------------------


def get_curve_exponent_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Curve:Exponent object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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
        osm_object = osm_model.getCurveExponent(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getCurveExponentByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle': str(target_object.handle()), 
                   'Name': target_object.nameString(), 
                   'Coefficient1 Constant': target_object.coefficient1Constant(), 
                   'Coefficient2 Constant': target_object.coefficient2Constant(), 
                   'Coefficient3 Constant': target_object.coefficient3Constant(), 
                   'Minimum Value of x': target_object.minimumValueofx(), 
                   'Maximum Value of x': target_object.maximumValueofx(), 
                   'Minimum Curve Output': target_object.minimumCurveOutput(), 
                   'Maximum Curve Output': target_object.maximumCurveOutput(), 
                   'Input Unit Type for X': target_object.inputUnitTypeforX(), 
                   'Output Unit Type': target_object.outputUnitType()}

    return object_dict

def get_all_curve_exponent_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Curve:Exponent objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a curve exponent object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getCurveExponents()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_curve_exponent_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_curve_exponent_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all curve exponent objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all curve exponent objects.
    """

    all_objects_dicts = get_all_curve_exponent_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Coefficient1 Constant', 'Coefficient2 Constant', 'Coefficient3 Constant', 'Minimum Value of x', 'Maximum Value of x', 'Minimum Curve Output', 'Maximum Curve Output', 'Input Unit Type for X', 'Output Unit Type']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all curve exponent objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} curve exponent objects.")

    return all_objects_df


# --------------------------------------------------
#  ***** OS:Curve:Quadratic ************************
# --------------------------------------------------


def get_curve_quadratic_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Curve:Quadratic object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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
        osm_object = osm_model.getCurveQuadratic(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getCurveQuadraticByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle': str(target_object.handle()), 
                   'Name': target_object.nameString(), 
                   'Coefficient1 Constant': target_object.coefficient1Constant(), 
                   'Coefficient2 x': target_object.coefficient2x(), 
                   'Coefficient3 x**2': target_object.coefficient3xPOW2(), 
                   'Minimum Value of x': target_object.minimumValueofx(), 
                   'Maximum Value of x': target_object.maximumValueofx()}

    return object_dict

def get_all_curve_quadratic_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Curve:Quadratic objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a curve quadratic object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getCurveQuadratics()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_curve_quadratic_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_curve_quadratic_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all curve quadratic objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all curve quadratic objects.
    """

    all_objects_dicts = get_all_curve_quadratic_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Coefficient1 Constant', 'Coefficient2 x', 'Coefficient3 x**2', 'Minimum Value of x', 'Maximum Value of x']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all curve quadratic objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} curve quadratic objects.")

    return all_objects_df