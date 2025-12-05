import openstudio
import pandas as pd

# ------------------------------------------------------------------------------------------------
#  ****** Template Functions *********************************************************************
# ------------------------------------------------------------------------------------------------


def get_osm_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve an object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    # Define the methods to retrieve objects by handle and name here
    get_object_method_by_handle = osm_model.getPeople
    get_object_method_by_name = osm_model.getPeopleByName

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = get_object_method_by_handle(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = get_object_method_by_name(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None
    }

    return object_dict

# ------------------------------------------------------------------------------------------------
#  ****** People *********************************************************************************
# ------------------------------------------------------------------------------------------------


def get_people_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a people object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified people object.
    """

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getPeople(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getPeopleByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'People Definition Name': target_object.peopleDefinition().nameString(),
        'Space or Space Type Name': target_object.spaceType().get().name().get() if not target_object.spaceType().isNull() else (target_object.space().get().name().get() if not target_object.space().isNull() else None),
        'Number of People': target_object.numberofPeopleSchedule().get().name().get() if not target_object.numberofPeopleSchedule().isNull() else None,
        'Number of People Schedule Name': target_object.numberofPeopleSchedule().get().name().get() if not target_object.numberofPeopleSchedule().isNull() else None,
        'Activity Level Schedule Name': target_object.activityLevelSchedule().get().name().get() if not target_object.activityLevelSchedule().isNull() else None,
        'Surface Name/Angle Factor List Name': None,
        'Work Efficiency Schedule Name': target_object.workEfficiencySchedule().get().name().get() if not target_object.workEfficiencySchedule().isNull() else None,
        'Clothing Insulation Schedule Name': target_object.clothingInsulationSchedule().get().name().get() if not target_object.clothingInsulationSchedule().isNull() else None,
        'Air Velocity Schedule Name': target_object.airVelocitySchedule().get().name().get() if not target_object.airVelocitySchedule().isNull() else None,
        'Multiplier': target_object.multiplier(),
        'Ankle Level Air Velocity Schedule Name': target_object.ankleLevelAirVelocitySchedule().get().name().get() if not target_object.ankleLevelAirVelocitySchedule().isNull() else None,
        'Cold Stress Temperature Threshold {C}': target_object.coldStressTemperatureThreshold(),
        'Heat Stress Temperature Threshold {C}': target_object.heatStressTemperatureThreshold()
    }

    return object_dict


def get_all_people_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all people objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a people object.
    """

    # Get all people objects in the OpenStudio model.
    all_objects = osm_model.getPeoples()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_people_object_as_dict(osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_people_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all people objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all people objects.
    """

    all_objects_dicts = get_all_people_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = [
        'Handle',
        'Name',
        'People Definition Name',
        'Space or Space Type Name',
        'Number of People',
        'Number of People Schedule Name',
        'Activity Level Schedule Name',
        'Surface Name/Angle Factor List Name',
        'Work Efficiency Schedule Name',
        'Clothing Insulation Schedule Name',
        'Air Velocity Schedule Name',
        'Multiplier',
        'Ankle Level Air Velocity Schedule Name',
        'Cold Stress Temperature Threshold {C}',
        'Heat Stress Temperature Threshold {C}'
    ]

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all people objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} people objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** People Definition **********************************************************************
# ------------------------------------------------------------------------------------------------


def get_people_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a people object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified people object.
    """

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getPeopleDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getPeopleDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()
    floorArea = target_object.floorArea()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Number of People Calculation Method': target_object.numberofPeopleCalculationMethod(),
        'Number of People {people}': target_object.getNumberOfPeople(floorArea),
        'People per Space Floor Area {person/m2}': 1 / target_object.getFloorAreaPerPerson(floorArea) if target_object.getNumberOfPeople(floorArea) != 0 else 0.0,
        'Space Floor Area per Person {m2/person}': target_object.getFloorAreaPerPerson(floorArea) if target_object.getNumberOfPeople(floorArea) != 0 else 0.0,
        'Fraction Radiant': target_object.fractionRadiant(),
        'Sensible Heat Fraction': target_object.sensibleHeatFraction() if not target_object.sensibleHeatFraction().isNull() else None,
        'Carbon Dioxide Generation Rate {m3/s-W}': target_object.carbonDioxideGenerationRate(),
        'Enable ASHRAE 55 Comfort Warnings': None}

    return object_dict


def get_all_people_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all people definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a people object.
    """

    # Get all people definition objects in the OpenStudio model.
    all_objects = osm_model.getPeopleDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_people_definition_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_people_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all people definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all people definition objects.
    """

    all_objects_dicts = get_all_people_definition_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = [
        'Handle',
        'Name',
        'Number of People Calculation Method',
        'Number of People {people}',
        'People per Space Floor Area {person/m2}',
        'Space Floor Area per Person {m2/person}',
        'Fraction Radiant',
        'Sensible Heat Fraction',
        'Carbon Dioxide Generation Rate {m3/s-W}',
        'Enable ASHRAE 55 Comfort Warnings'
    ]

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all people definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} people definition objects")

    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Lights *********************************************************************************
# ------------------------------------------------------------------------------------------------


def get_lights_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a light object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified light object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getLights(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getLightsByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Lights Definition Name': target_object.lightsDefinition().name().get() if not target_object.lightsDefinition().name().isNull() else None,
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if not target_object.spaceType().isNull() else
        (target_object.space().get().name().get()
         if not target_object.space().isNull() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Fraction Replaceable': target_object.fractionReplaceable(),
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict


def get_all_lights_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all light objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a light object.
    """

    # Get all light objects in the OpenStudio model.
    all_objects = osm_model.getLightss()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_lights_object_as_dict(osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_lights_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all light objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all light objects.
    """

    all_objects_dicts = get_all_lights_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = [
        'Handle',
        'Name',
        'Lights Definition Name',
        'Space or SpaceType Name',
        'Schedule Name',
        'Fraction Replaceable',
        'Multiplier',
        'End-Use Subcategory'
    ]

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all light objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} light objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Lights Definition **********************************************************************
# ------------------------------------------------------------------------------------------------

def get_lights_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a lights definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified lights definition object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getLightsDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getLightsDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()
    floorArea = target_object.floorArea()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Light Definition Name': target_object.nameString(),
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Lighting Level {W}': target_object.lightingLevel().get() if not target_object.lightingLevel().isNull() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if not target_object.wattsperSpaceFloorArea().isNull() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if not target_object.wattsperPerson().isNull() else None,
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Visible': target_object.fractionVisible(),
        'Return Air Fraction': target_object.returnAirFraction()
    }

    return object_dict


def get_all_lights_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all lights definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a lights definition object.
    """

    # Get all lights definition objects in the OpenStudio model.
    all_objects = osm_model.getLightsDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_lights_definition_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_lights_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all lights definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all lights definition objects.
    """

    all_objects_dicts = get_all_lights_definition_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = [
        'Handle',
        'Name',
        'Light Definition Name',
        'Design Level Calculation Method',
        'Lighting Level {W}',
        'Watts per Space Floor Area {W/m2}',
        'Watts per Person {W/person}',
        'Fraction Radiant',
        'Fraction Visible',
        'Return Air Fraction'
    ]

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all lights definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} lights definition objects")

    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Electric Equipment *********************************************************************************
# ------------------------------------------------------------------------------------------------


def get_electric_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve an electric equipment object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified electric equipment object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getElectricEquipment(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getElectricEquipmentByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Electric Equipment Definition Name': target_object.definition().nameString(),
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if not target_object.spaceType().isNull() else (target_object.space().get().name().get() if not target_object.space().isNull() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict


def get_all_electric_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all electric equipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an electric equipment object.
    """

    # Get all electric equipment objects in the OpenStudio model.
    all_objects = osm_model.getElectricEquipments()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_electric_equipment_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_electric_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all electric equipment objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all electric equipment objects.
    """

    all_objects_dicts = get_all_electric_equipment_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Electric Equipment Definition Name',
               'Space or SpaceType Name', 'Schedule Name', 'Multiplier', 'End-Use Subcategory']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all electric equipment objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} electric equipment objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Electric Equipment Definition **********************************************************
# ------------------------------------------------------------------------------------------------

def get_electric_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve an electric equipment definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified electric equipment definition object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getElectricEquipmentDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getElectricEquipmentDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': target_object.designLevel().get() if not target_object.designLevel().isNull() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if not target_object.wattsperSpaceFloorArea().isNull() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if not target_object.wattsperPerson().isNull() else None,
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }

    return object_dict


def get_all_electric_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all electric equipment definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an electric equipment definition object.
    """

    # Get all electric equipment definition objects in the OpenStudio model.
    all_objects = osm_model.getElectricEquipmentDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_electric_equipment_definition_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_electric_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all electric equipment definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all electric equipment definition objects.
    """

    all_objects_dicts = get_all_electric_equipment_definition_objects_as_dicts(
        osm_model)

    # Define the columns for the DataFrame
    columns = [
        'Handle',
        'Name',
        'Design Level Calculation Method',
        'Design Level {W}',
        'Watts per Space Floor Area {W/m2}',
        'Watts per Person {W/person}',
        'Fraction Latent',
        'Fraction Radiant',
        'Fraction Lost'
    ]

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all electric equipment definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} electric equipment definition objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Gas Equipment **************************************************************************
# ------------------------------------------------------------------------------------------------

def get_gas_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a gas equipment object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified gas equipment object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getGasEquipment(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getGasEquipmentByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Gas Equipment Definition Name': target_object.definition().nameString(),
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if not target_object.spaceType().isNull() else (target_object.space().get().name().get() if not target_object.space().isNull() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict


def get_all_gas_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all gas equipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a gas equipment object.
    """

    # Get all gas equipment objects in the OpenStudio model.
    all_objects = osm_model.getGasEquipments()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_gas_equipment_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_gas_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all gas equipment objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all gas equipment objects.
    """

    all_objects_dicts = get_all_gas_equipment_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Gas Equipment Definition Name',
               'Space or SpaceType Name', 'Schedule Name', 'Multiplier', 'End-Use Subcategory']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all gas equipment objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} gas equipment objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Gas Equipment Definition ***************************************************************
# ------------------------------------------------------------------------------------------------


def get_gas_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a gas equipment definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified gas equipment definition object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getGasEquipmentDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getGasEquipmentDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': target_object.designLevel().get() if not target_object.designLevel().isNull() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if not target_object.wattsperSpaceFloorArea().isNull() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if not target_object.wattsperPerson().isNull() else None,
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }

    return object_dict


def get_all_gas_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all gas equipment definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a gas equipment definition object.
    """

    # Get all gas equipment definition objects in the OpenStudio model.
    all_objects = osm_model.getGasEquipmentDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_gas_equipment_definition_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_gas_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all gas equipment definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all gas equipment definition objects.
    """

    all_objects_dicts = get_all_gas_equipment_definition_objects_as_dicts(
        osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Design Level Calculation Method',
               'Design Level {W}', 'Watts per Space Floor Area {W/m2}', 'Watts per Person {W/person}', 'Fraction Latent', 'Fraction Radiant', 'Fraction Lost']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all gas equipment definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} gas equipment definition objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Steam Equipment ************************************************************************
# ------------------------------------------------------------------------------------------------
def get_steam_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a steam equipment object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified steam equipment object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getSteamEquipment(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getSteamEquipmentByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Steam Equipment Definition Name': target_object.definition().nameString(),
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if not target_object.spaceType().isNull() else (target_object.space().get().name().get() if not target_object.space().isNull() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict


def get_all_steam_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all steam equipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a steam equipment object.
    """

    # Get all steam equipment objects in the OpenStudio model.
    all_objects = osm_model.getSteamEquipments()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_steam_equipment_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_steam_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all steam equipment objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all steam equipment objects.
    """

    all_objects_dicts = get_all_steam_equipment_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Steam Equipment Definition Name',
               'Space or SpaceType Name', 'Schedule Name', 'Multiplier', 'End-Use Subcategory']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all steam equipment objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} steam equipment objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Steam Equipment Definition *************************************************************
# ------------------------------------------------------------------------------------------------

def get_steam_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a steam equipment definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified steam equipment definition object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getSteamEquipmentDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getSteamEquipmentDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': target_object.designLevel().get() if not target_object.designLevel().isNull() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if not target_object.wattsperSpaceFloorArea().isNull() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if not target_object.wattsperPerson().isNull() else None,
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }

    return object_dict


def get_all_steam_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all steam equipment definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a steam equipment definition object.
    """

    # Get all steam equipment definition objects in the OpenStudio model.
    all_objects = osm_model.getSteamEquipmentDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_steam_equipment_definition_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_steam_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all steam equipment definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all steam equipment definition objects.
    """

    all_objects_dicts = get_all_steam_equipment_definition_objects_as_dicts(
        osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Design Level Calculation Method',
               'Design Level {W}', 'Watts per Space Floor Area {W/m2}', 'Watts per Person {W/person}', 'Fraction Latent', 'Fraction Radiant', 'Fraction Lost']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all steam equipment definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} steam equipment definition objects")

    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Other Equipment ************************************************************************
# ------------------------------------------------------------------------------------------------


def get_other_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve an other equipment object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified other equipment object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getOtherEquipment(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getOtherEquipmentByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Other Equipment Definition Name': None,
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if not target_object.spaceType().isNull() else (target_object.space().get().name().get() if not target_object.space().isNull() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'Fuel Type': target_object.fuelType(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict


def get_all_other_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all other equipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an other equipment object.
    """

    # Get all other equipment objects in the OpenStudio model.
    all_objects = osm_model.getOtherEquipments()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_other_equipment_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_other_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all other equipment objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all other equipment objects.
    """

    all_objects_dicts = get_all_other_equipment_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Other Equipment Definition Name',
               'Space or SpaceType Name', 'Schedule Name', 'Multiplier', 'Fuel Type', 'End-Use Subcategory']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all other equipment objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} other equipment objects")

    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Other Equipment Definition *************************************************************
# ------------------------------------------------------------------------------------------------


def get_other_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve an other equipment definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified other equipment definition object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getOtherEquipmentDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getOtherEquipmentDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': target_object.designLevel().get() if not target_object.designLevel().isNull() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if not target_object.wattsperSpaceFloorArea().isNull() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if not target_object.wattsperPerson().isNull() else None,
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }

    return object_dict


def get_all_other_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all other equipment definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an other equipment definition object.
    """

    # Get all other equipment definition objects in the OpenStudio model.
    all_objects = osm_model.getOtherEquipmentDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_other_equipment_definition_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_other_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all other equipment definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all other equipment definition objects.
    """

    all_objects_dicts = get_all_other_equipment_definition_objects_as_dicts(
        osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Design Level Calculation Method',
               'Design Level {W}', 'Watts per Space Floor Area {W/m2}', 'Watts per Person {W/person}', 'Fraction Latent', 'Fraction Radiant', 'Fraction Lost']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all other equipment definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} other equipment definition objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Water Use Equipment ********************************************************************
# ------------------------------------------------------------------------------------------------


def get_water_use_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a water use equipment object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified water use equipment object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getWaterUseEquipment(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getWaterUseEquipmentByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Water Use Equipment Definition Name': target_object.definition().nameString(),
        'Space Name': target_object.space().get().name().get() if not target_object.space().isNull() else None,
        'Flow Rate Fraction Schedule Name': target_object.flowRateFractionSchedule().get().name().get() if not target_object.flowRateFractionSchedule().isNull() else None
    }

    return object_dict


def get_all_water_use_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all water use equipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a water use equipment object.
    """

    # Get all water use equipment objects in the OpenStudio model.
    all_objects = osm_model.getWaterUseEquipments()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_water_use_equipment_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_water_use_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all water use equipment objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all water use equipment objects.
    """

    all_objects_dicts = get_all_water_use_equipment_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Water Use Equipment Definition Name',
               'Space Name', 'Flow Rate Fraction Schedule Name']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all water use equipment objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} water use equipment objects")

    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Water Use Equipment Definition *********************************************************
# ------------------------------------------------------------------------------------------------


def get_water_use_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a water use equipment definition object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified water use equipment definition object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the object by handle or name
    if handle is not None:
        osm_object = osm_model.getWaterUseEquipmentDefinition(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getWaterUseEquipmentDefinitionByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'End-Use Subcategory': target_object.endUseSubcategory(),
        'Peak Flow Rate {m3/s}': target_object.peakFlowRate(),
        'Target Temperature Schedule Name': target_object.targetTemperatureSchedule().get().name().get() if not target_object.targetTemperatureSchedule().isNull() else None,
        'Sensible Fraction Schedule Name': target_object.sensibleFractionSchedule().get().name().get() if not target_object.sensibleFractionSchedule().isNull() else None,
        'Latent Fraction Schedule Name': target_object.latentFractionSchedule().get().name().get() if not target_object.latentFractionSchedule().isNull() else None
    }

    return object_dict


def get_all_water_use_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all water use equipment definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a water use equipment definition object.
    """

    # Get all water use equipment definition objects in the OpenStudio model.
    all_objects = osm_model.getWaterUseEquipmentDefinitions()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_water_use_equipment_definition_object_as_dict(
            osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_water_use_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all water use equipment definition objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all water use equipment definition objects.
    """

    all_objects_dicts = get_all_water_use_equipment_definition_objects_as_dicts(
        osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'End-Use Subcategory',
               'Peak Flow Rate {m3/s}', 'Target Temperature Schedule Name', 'Sensible Fraction Schedule Name', 'Latent Fraction Schedule Name']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all water use equipment definition objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} water use equipment definition objects")

    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Space Infiltration Design Flow Rate ****************************************************
# ------------------------------------------------------------------------------------------------


def get_space_infiltration_design_flowrate_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a space infiltration design flow rate object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the space infiltration design flow rate object to retrieve.
    - name (str, optional): The name of the space infiltration design flow rate object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified space infiltration design flow rate object.
    """

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the space infiltration design flow rate object by handle or name
    if handle is not None:
        osm_object = osm_model.getSpaceInfiltrationDesignFlowRate(
            handle)
        if osm_object is None:
            print(
                f"No space infiltration design flow rate object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getSpaceInfiltrationDesignFlowRateByName(
            name)
        if not osm_object:
            print(
                f"No space infiltration design flow rate object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if not target_object.spaceType().isNull() else (target_object.space().get().name().get() if not target_object.space().isNull() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Design Flow Rate Calculation Method': target_object.designFlowRateCalculationMethod(),
        'Design Flow Rate {m3/s}': target_object.designFlowRate().get() if target_object.designFlowRate().is_initialized() else None,
        'Flow per Space Floor Area {m3/s-m2}': target_object.flowperSpaceFloorArea().get() if target_object.flowperSpaceFloorArea().is_initialized() else None,
        'Flow per Exterior Surface Area {m3/s-m2}': target_object.flowperExteriorSurfaceArea().get() if target_object.flowperExteriorSurfaceArea().is_initialized()
        else (target_object.flowperExteriorWallArea().get() if target_object.flowperExteriorWallArea().is_initialized() else None),
        'Air Changes per Hour {1/hr}': target_object.airChangesperHour().get() if target_object.airChangesperHour().is_initialized() else None,
        'Constant Term Coefficient': target_object.constantTermCoefficient(),
        'Temperature Term Coefficient': target_object.temperatureTermCoefficient(),
        'Velocity Term Coefficient': target_object.velocityTermCoefficient(),
        'Velocity Squared Term Coefficient': target_object.velocitySquaredTermCoefficient()
    }

    return object_dict


def get_all_space_infiltration_design_flowrate_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all space infiltration design flow rate objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space infiltration design flow rate object.
    """

    # Get all space infiltration design flow rate objects in the OpenStudio model.
    all_objects = osm_model.getSpaceInfiltrationDesignFlowRates()

    all_objects_dicts = []

    for target_object in all_objects:
        handle = str(target_object.handle())
        object_dict = get_space_infiltration_design_flowrate_object_as_dict(
            osm_model, handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_space_infiltration_design_flowrate_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all space infiltration design flow rate objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all space infiltration design flow rate objects.
    """

    all_objects_dicts = get_all_space_infiltration_design_flowrate_objects_as_dicts(
        osm_model)

    # Define the columns for the DataFrame
    columns = [
        'Handle',
        'Name',
        'Space or SpaceType Name',
        'Schedule Name',
        'Design Flow Rate Calculation Method',
        'Design Flow Rate {m3/s}',
        'Flow per Space Floor Area {m3/s-m2}',
        'Flow per Exterior Surface Area {m3/s-m2}',
        'Air Changes per Hour {1/hr}',
        'Constant Term Coefficient',
        'Temperature Term Coefficient',
        'Velocity Term Coefficient',
        'Velocity Squared Term Coefficient'
    ]

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all space infiltration design flow rate objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} space infiltration design flow rate objects")

    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Design Specification Outdoor Air *******************************************************
# ------------------------------------------------------------------------------------------------


def get_design_specification_outdoor_air_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a design specification outdoor air object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the design specification outdoor air object to retrieve.
    - name (str, optional): The name of the design specification outdoor air object to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified design specification outdoor air object.
    """

    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

    # Find the design specification outdoor air object by handle or name
    if handle is not None:
        osm_object = osm_model.getDesignSpecificationOutdoorAir(handle)
        if osm_object is None:
            print(
                f"No design specification outdoor air object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getDesignSpecificationOutdoorAirByName(name)
        if not osm_object:
            print(
                f"No design specification outdoor air object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Outdoor Air Method': target_object.outdoorAirMethod(),
        'Outdoor Air Flow per Person {m3/s-person}': target_object.outdoorAirFlowperPerson(),
        'Outdoor Air Flow per Floor Area {m3/s-m2}': target_object.outdoorAirFlowperFloorArea(),
        'Outdoor Air Flow Rate {m3/s}': target_object.outdoorAirFlowRate(),
        'Outdoor Air Flow Air Changes per Hour {1/hr}': target_object.outdoorAirFlowAirChangesperHour(),
        'Outdoor Air Flow Rate Fraction Schedule Name': target_object.outdoorAirFlowRateFractionSchedule().get().name() if not target_object.outdoorAirFlowRateFractionSchedule().isNull() else None

    }

    return object_dict


def get_all_design_specification_outdoor_air_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all design specification outdoor air objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a design specification outdoor air object.
    """

    # Get all design specification outdoor air objects in the OpenStudio model.
    all_objects = osm_model.getDesignSpecificationOutdoorAirs()

    all_objects_dicts = []

    for target_object in all_objects:
        handle = str(target_object.handle())
        object_dict = get_design_specification_outdoor_air_object_as_dict(
            osm_model, handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_design_specification_outdoor_air_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all design specification outdoor air objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all design specification outdoor air objects.
    """

    all_objects_dicts = get_all_design_specification_outdoor_air_objects_as_dicts(
        osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Outdoor Air Method', 'Outdoor Air Flow per Person {m3/s-person}', 'Outdoor Air Flow per Floor Area {m3/s-m2}',
               'Outdoor Air Flow Rate {m3/s}', 'Outdoor Air Flow Air Changes per Hour {1/hr}', 'Outdoor Air Flow Rate Fraction Schedule Name']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all design specification outdoor air objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} design specification outdoor air objects")

    return all_objects_df
