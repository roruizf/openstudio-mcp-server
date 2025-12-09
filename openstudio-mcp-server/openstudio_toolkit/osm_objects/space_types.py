import openstudio
import pandas as pd
import numpy as np
from openstudio_toolkit.osm_objects.schedules import *


def get_all_space_types_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all space types objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all space types objects.
    """

    # Get all spaces in the OpenStudio model.
    all_space_types = osm_model.getSpaceTypes()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_space_types],
        'Name': [x.name().get() for x in all_space_types],
        'Default Construction Set Name': [x.defaultConstructionSet().get().name().get() if not x.defaultConstructionSet().isNull() else None for x in all_space_types],
        'Default Schedule Set Name': [x.defaultScheduleSet().get().name().get() if not x.defaultScheduleSet().isNull() else None for x in all_space_types],
        'Group Rendering Name': [x.renderingColor().get().name().get() if not x.renderingColor().isNull() else None for x in all_space_types],
        'Design Specification Outdoor Air Object Name': [x.designSpecificationOutdoorAir().get().name().get() if not x.designSpecificationOutdoorAir().isNull() else None for x in all_space_types],
        'Standards Template': [x.standardsTemplate().get() if not x.standardsTemplate().isNull() else None for x in all_space_types],
        'Standards Building Type': [x.standardsBuildingType().get() if not x.standardsBuildingType().isNull() else None for x in all_space_types],
        'Standards Space Type': [x.standardsSpaceType().get() if not x.standardsSpaceType().isNull() else None for x in all_space_types]
    }

    # Create a DataFrame of all space types.
    all_space_types_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_space_types_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_space_types_df = all_space_types_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_space_types_df.shape[0]} space types")

    return all_space_types_df



def get_space_type_as_dict(osm_model: openstudio.model.Model, space_type_handle: str = None, space_type_name: str = None) -> dict:
    """
    Retrieve a space from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_handle (str, optional): The handle of the space to retrieve.
    - space_name (str, optional): The name of the space to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified space.
    """
    if space_type_handle is None and space_type_name is None:
        raise ValueError("Either 'space_type_handle' or 'space_type_name' must be provided.")
    
    # Find the space_type by handle or name
    if space_type_handle is not None:
        space_type_object = osm_model.getSpaceType(space_type_handle)
        if space_type_object.isNull():
            print(f"No space found with the handle: {space_type_handle}")
            return {}
    elif space_type_name is not None:
        space_type_object = osm_model.getSpaceTypeByName(space_type_name)
        if space_type_object.isNull():
            print(f"No space found with the name: {space_type_name}")
            return {}

    target_space_type = space_type_object.get()
    
    space_type_dict ={
        'Handle': str(target_space_type.handle()) ,
        'Name': target_space_type.nameString() ,
        'Rendering Color': target_space_type.renderingColor().get().name().get() if not target_space_type.renderingColor().isNull() else None ,
        'Default Construction Set': target_space_type.defaultConstructionSet().get().name().get() if not target_space_type.defaultConstructionSet().isNull() else None ,
        'Default Schedule Set': target_space_type.defaultScheduleSet().get().name().get() if not target_space_type.defaultScheduleSet().isNull() else None ,
        # Design Specification Outdoor Air
        'Design Specification Outdoor Air': target_space_type.designSpecificationOutdoorAir().get().name().get() if not target_space_type.designSpecificationOutdoorAir().isNull() else None ,
        # Infiltration
        'Space Infiltration Design Flow Rates': target_space_type.spaceInfiltrationDesignFlowRates()[0].name().get() if target_space_type.spaceInfiltrationDesignFlowRates() else None ,
        'Space Infiltration Effective Leakage Area': target_space_type.spaceInfiltrationEffectiveLeakageAreas()[0].name().get() if target_space_type.spaceInfiltrationEffectiveLeakageAreas() else None ,
        # People
        'People Load Name': target_space_type.people()[0].name().get() if target_space_type.people() else None ,
        'People Definition': target_space_type.people()[0].definition().name().get() if target_space_type.people() else None ,
        'People Number Of People Schedule': target_space_type.defaultScheduleSet().get().numberofPeopleSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().numberofPeopleSchedule().isNull() else None ,
        'People Activity Level Schedule': target_space_type.defaultScheduleSet().get().peopleActivityLevelSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().peopleActivityLevelSchedule().isNull() else None ,
        # Lights
        'Lights Load Name': target_space_type.lights()[0].name().get() if target_space_type.lights() else None ,
        'Lights Definition': target_space_type.lights()[0].definition().name().get() if target_space_type.lights() else None ,
        'Lighting Schedule': target_space_type.defaultScheduleSet().get().lightingSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().lightingSchedule().isNull() else None ,
        # Luminaires
        'Luminaires Load Name': target_space_type.luminaires()[0].name().get() if target_space_type.luminaires() else None ,
        'Luminaires Definition': target_space_type.luminaires()[0].definition().name().get() if target_space_type.luminaires() else None ,
        'Luminaires Schedule': None, #target_space_type.defaultScheduleSet().get().lightingSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().lightingSchedule().isNull() else None ,
        # Electric Equipment
        'Electric Equipment Load Name': target_space_type.electricEquipment()[0].name().get() if target_space_type.electricEquipment() else None ,
        'Electric Equipment Definition': target_space_type.electricEquipment()[0].definition().name().get() if target_space_type.electricEquipment() else None ,
        'Electric Equipment Schedule': target_space_type.defaultScheduleSet().get().electricEquipmentSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().electricEquipmentSchedule().isNull() else None ,
        # Gas Equipment        
        'Gas Equipment Load Name': target_space_type.gasEquipment()[0].name().get() if target_space_type.gasEquipment() else None ,
        'Gas Equipment Definition': target_space_type.gasEquipment()[0].definition().name().get() if target_space_type.gasEquipment() else None ,
        'Gas Equipment Schedule': target_space_type.defaultScheduleSet().get().gasEquipmentSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().gasEquipmentSchedule().isNull() else None ,
        # Steam Equipment        
        'Steam Equipment Load Name': target_space_type.steamEquipment()[0].name().get() if target_space_type.steamEquipment() else None ,
        'Steam Equipment Definition': target_space_type.steamEquipment()[0].definition().name().get() if target_space_type.steamEquipment() else None ,
        'Steam Equipment Schedule': target_space_type.defaultScheduleSet().get().steamEquipmentSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().steamEquipmentSchedule().isNull() else None ,
        # Other Equipment        
        'Other Equipment Load Name': target_space_type.otherEquipment()[0].name().get() if target_space_type.otherEquipment() else None ,
        'Other Equipment Definition': target_space_type.otherEquipment()[0].definition().name().get() if target_space_type.otherEquipment() else None ,
        'Other Equipment Schedule': target_space_type.defaultScheduleSet().get().otherEquipmentSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().otherEquipmentSchedule().isNull() else None ,
        # Internal Mass Definitions
        'Internal Mass Name': target_space_type.internalMass()[0].name().get() if target_space_type.internalMass() else None,
        'Internal Mass Definition': target_space_type.internalMass()[0].definition().name().get() if target_space_type.internalMass() else None,
        # Infiltration
        'Infiltration Schedule': target_space_type.defaultScheduleSet().get().infiltrationSchedule().get().name().get() if not target_space_type.defaultScheduleSet().isNull() and not target_space_type.defaultScheduleSet().get().infiltrationSchedule().isNull() else None 
        }
    
    return space_type_dict

def get_all_space_types_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all spaces types from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space types.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getSpaceTypes()

    all_objects_dicts = []

    for target_object in all_objects:
        space_type_handle = str(target_object.handle())
        object_dict = get_space_type_as_dict(osm_model, space_type_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_space_types_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all space types from the OpenStudio model using a specified method and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all space types.
    """

    all_objects_dicts = get_all_space_types_as_dicts(osm_model)

    # Create a DataFrame of all spaces.
    all_space_types_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_space_types_df = all_space_types_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_space_types_df.shape[0]} spaces")

    return all_space_types_df

def create_new_space_types_objects(osm_model: openstudio.model.Model, space_types_to_create_df: pd.DataFrame) -> openstudio.model.Model:
    """
    Create new space types components based on data from a New Objects DataFrame.

    Parameters:
    - osm_model: The OpenStudio Model object.
    - space_types_to_create_df: DataFrame containing data for new building story components.

    Returns:
    - osm_model: The OpenStudio Model object.
    """
    space_types_to_create_df = space_types_to_create_df.replace(np.nan, None)

    for _, row in space_types_to_create_df.iterrows():

        # Create new Space Type
        new_space_type = openstudio.model.SpaceType(osm_model)
        new_space_type.setName(row['Name'])

        if new_space_type.nameString() != row['Name']:
            print(f"Space type Name set {new_space_type.nameString()} is different than defined: {row['Name']}")

        # Setting attributes if defined in space_types_to_create_df

        # Default Construction Set Name
        if row['Default Construction Set Name'] is not None:
          if osm_model.getDefaultConstructionSetByName(row['Default Construction Set Name']).isNull():
            new_construction_set = openstudio.model.DefaultConstructionSet(
                  osm_model)
            new_space_type.setDefaultConstructionSet(new_construction_set)
        
        # Default Schedule Set Name
        if row['Default Schedule Set Name'] is not None:
            new_schedule_set = openstudio.model.DefaultScheduleSet(osm_model)
            new_space_type.setDefaultScheduleSet(new_schedule_set)
        
        # Group Rendering Name   
        if row['Group Rendering Name'] is not None:
            if osm_model.getRenderingColorByName(row['Group Rendering Name']).isNull():
                rendering_color = openstudio.model.RenderingColor(osm_model)
            else:
                rendering_color = osm_model.getRenderingColorByName(row['Group Rendering Name']).get()

            rendering_color.setName(row['Group Rendering Name'])
            new_space_type.setRenderingColor(rendering_color)
       
        # Design Specification Outdoor Air Object Name
        if row['Design Specification Outdoor Air Object Name'] is not None:
            pass
        
        # Standards Template	
        # Standards Building Type	
        # Standards Space Type

        new_space_type.setName(row['Name'])   

    print(f"{space_types_to_create_df.shape[0]} new space types objects created")
    
    return osm_model

def rename_space_types_components(osm_model: openstudio.model.Model, space_type_name_list: list) -> None:

    # Get all space types
    all_space_types_df = get_all_space_types_as_dataframe(osm_model)
    all_space_types_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    for index, row in all_space_types_df.iterrows():
       
        space_type_name = row['Name']
        space_type_handle = row['Handle']

        # Get Space Type row by row
        target_space_type = osm_model.getSpaceType(row['Handle']).get()

        print(f"{index + 1}. {space_type_name}:")
        
        for column in all_space_types_df.drop(columns=['Handle', 'Name']).columns: 

            new_name = f"{space_type_name} {column.replace('Name', '').replace('Load', '')}"
            if row[column] is not None and row[column] != new_name:
                if column == 'Rendering Color':
                    target_space_type.renderingColor().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.renderingColor().get().nameString()}")
                elif column == 'Default Construction Set':
                    target_space_type.defaultConstructionSet().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultConstructionSet().get().nameString()}")
                elif column == 'Default Schedule Set':
                    target_space_type.defaultScheduleSet().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().nameString()}")
                elif column == 'Design Specification Outdoor Air':
                    target_space_type.designSpecificationOutdoorAir().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.designSpecificationOutdoorAir().get().nameString()}")
                elif column == 'Space Infiltration Design Flow Rates':
                    target_space_type.spaceInfiltrationDesignFlowRates()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.spaceInfiltrationDesignFlowRates()[0].nameString()}")
                elif column == 'Space Infiltration Effective Leakage Area':
                    target_space_type.spaceInfiltrationEffectiveLeakageArea()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.spaceInfiltrationEffectiveLeakageArea()[0].nameString()}")
                elif column == 'People Load Name':
                    target_space_type.people()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.people()[0].nameString()}")
                elif column == 'People Definition':
                    target_space_type.people()[0].definition().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.people()[0].definition().nameString()}")
                elif column == 'People Number Of People Schedule':
                    target_space_type.defaultScheduleSet().get().numberofPeopleSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().numberofPeopleSchedule().get().nameString()}")
                elif column == 'People Activity Level Schedule':
                    target_space_type.defaultScheduleSet().get().peopleActivityLevelSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().peopleActivityLevelSchedule().get().nameString()}")
                elif column == 'Lights Load Name':
                    target_space_type.lights()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.lights()[0].nameString()}")
                elif column == 'Lights Definition':
                    target_space_type.lights()[0].definition().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.lights()[0].definition().nameString()}")
                elif column == 'Lighting Schedule':
                    target_space_type.defaultScheduleSet().get().lightingSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().lightingSchedule().get().nameString()}")
                elif column == 'Luminaires Load Name':
                    target_space_type.luminaires()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.luminaires()[0].nameString()}")
                elif column == 'Luminaires Definition':
                    target_space_type.luminaires()[0].definition().setName(new_name)
                elif column == 'Luminaires Schedule':
                    pass
                elif column == 'Electric Equipment Load Name':
                    target_space_type.electricEquipment()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.electricEquipment()[0].nameString()}")
                elif column == 'Electric Equipment Definition':
                    target_space_type.electricEquipment()[0].definition().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.electricEquipment()[0].definition().nameString()}")
                elif column == 'Electric Equipment Schedule':
                    target_space_type.defaultScheduleSet().get().electricEquipmentSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().electricEquipmentSchedule().get().nameString()}")
                elif column == 'Gas Equipment Load Name':
                    target_space_type.gasEquipment()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.gasEquipment()[0].nameString()}")
                elif column == 'Gas Equipment Definition':
                    target_space_type.gasEquipment()[0].definition().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.gasEquipment()[0].definition().nameString()}")
                elif column == 'Gas Equipment Schedule':
                    target_space_type.defaultScheduleSet().get().gasEquipmentSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().gasEquipmentSchedule().get().nameString()}")
                elif column == 'Steam Equipment Load Name':
                    target_space_type.steamEquipment()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.steamEquipment()[0].nameString()}")
                elif column == 'Steam Equipment Definition':
                    target_space_type.steamEquipment()[0].definition().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.steamEquipment()[0].definition().nameString()}")
                elif column == 'Steam Equipment Schedule':
                    target_space_type.defaultScheduleSet().get().steamEquipmentSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().steamEquipmentSchedule().get().nameString()}")
                elif column == 'Other Equipment Load Name':
                    target_space_type.otherEquipment()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.otherEquipment()[0].nameString()}")
                elif column == 'Other Equipment Definition':
                    target_space_type.otherEquipment()[0].definition().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.otherEquipment()[0].definition().nameString()}")
                elif column == 'Other Equipment Schedule':
                    target_space_type.defaultScheduleSet().get().otherEquipmentSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().otherEquipmentSchedule().get().nameString()}")
                elif column == 'Internal Mass Name':
                    target_space_type.internalMass()[0].setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.internalMass()[0].nameString()}")
                elif column == 'Internal Mass Definition':
                    target_space_type.internalMass()[0].definition().setName(new_name)   
                elif column == 'Infiltration Schedule':
                    target_space_type.defaultScheduleSet().get().infiltrationSchedule().get().setName(new_name)
                    print(f"    * {column} changed: from {row[column]} to {target_space_type.defaultScheduleSet().get().nameString()}")
                else:
                    pass


    


def create_complete_edit_space_types_components(osm_model: openstudio.model.Model, space_type_name_list: list, create_if_none: bool = False) -> openstudio.model.Model:

    # Rename all space types components
    rename_space_types_components(osm_model, space_type_name_list)

    # Get all space types
    all_space_types_df = get_all_space_types_as_dataframe(osm_model)
    all_space_types_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    # Default Schedule Set
    for index, row in all_space_types_df.iterrows():
        new_name = f"{row['Name']} Schedule Set"
        # Create a new object and assig it
        if (create_if_none and row['Default Schedule Set'] == None) or (row['Default Schedule Set'] != None and row['Default Schedule Set'] != new_name):
            # Create new object
            new = openstudio.model.DefaultScheduleSet(osm_model)
            new.setName(new_name)
            print(f"* Default Schedule Set: {new.name()} - created")
            # Assign it to the corresponding space type
            osm_model.getSpaceTypeByName(
                row['Name']).get().setDefaultScheduleSet(new)
            print(f"* Default Schedule Set: {new.name()} - assigned")

    # Design Specification Outdoor Air
    for index, row in all_space_types_df.iterrows():
        new_name = f"{row['Name']} Ventilation"
        # Create a new object and assig it
        if (create_if_none and row['Design Specification Outdoor Air'] == None) or (row['Design Specification Outdoor Air'] != None and row['Design Specification Outdoor Air'] != new_name):
            # Create new object
            new = openstudio.model.DesignSpecificationOutdoorAir(osm_model)
            new.setName(new_name)
            new.setOutdoorAirFlowAirChangesperHour(0)
            print(
                f"* Design Specification Outdoor Air: {new.name()} - created")
            # Assign it to the corresponding space type
            osm_model.getSpaceTypeByName(row['Name']).get(
            ).setDesignSpecificationOutdoorAir(new)
            print(
                f"* Design Specification Outdoor Air: {new.name()} - assigned")

    # Space Infiltration Design Flow Rates
    for index, row in all_space_types_df.iterrows():
        new_name = f"{row['Name']} Infiltration"
        # Create a new object and assig it
        if (create_if_none and row['Space Infiltration Design Flow Rates'] == None) or (row['Space Infiltration Design Flow Rates'] != None and row['Space Infiltration Design Flow Rates'] != new_name):
            new = openstudio.model.SpaceInfiltrationDesignFlowRate(osm_model)
            new.setName(new_name)
            new.setAirChangesperHour(0)
            print(
                f"* Space Infiltration Design Flow Rates: {new.name()} - created")
            # Assign it to the corresponding space type - In this case, space type is assigned to Space Infiltration Design Flow Rate
            new.setSpaceType(osm_model.getSpaceTypeByName(row['Name']).get())
            print(
                f"* Space Infiltration Design Flow Rates: {new.name()} - assigned")
    # Space Infiltration Effective Leakage Area
            # pass

    # People & People Definition
    for index, row in all_space_types_df.iterrows():
        people_new_name = f"{row['Name']} People"
        people_definition_new_name = f"{row['Name']} People Definition"
        # Create a new object and assig it
        if (create_if_none and row['People Load Name'] == None) or (row['People Load Name'] != None and row['People Load Name'] != people_new_name):
            # Create People:Definition object first
            people_definition = openstudio.model.PeopleDefinition(osm_model)
            people_definition.setName(people_definition_new_name)
            people_definition.setNumberofPeople(0)
            print(f"* People Definition: {people_definition.name()} - created")
            # Create People object from People:Definition
            people = openstudio.model.People(people_definition)
            people.setName(people_new_name)
            print(f"* People: {people.name()} - created")
            print(
                f"* People Definition: {people_definition.name()} - assigned")
            # Assign it to the corresponding space type - In this case, space type is assigned to People
            people.setSpaceType(
                osm_model.getSpaceTypeByName(row['Name']).get())
            print(f"* People: {people.name()} - assigned")

    # Lights & Lights Definition
    for index, row in all_space_types_df.iterrows():
        lights_new_name = f"{row['Name']} Lights"
        lights_definition_new_name = f"{row['Name']} Lights Definition"
        # Create a new object and assig it
        if (create_if_none and row['Lights Load Name'] == None) or (row['Lights Load Name'] != None and row['Lights Load Name'] != lights_new_name):
            # Create Lights:Definition object first
            lights_definition = openstudio.model.LightsDefinition(osm_model)
            lights_definition.setName(lights_definition_new_name)
            lights_definition.setLightingLevel(0)
            print(f"* Lights Definition: {lights_definition.name()} - created")
            # Create Lights object from Lights:Definition
            lights = openstudio.model.Lights(lights_definition)
            lights.setName(lights_new_name)
            print(f"* Lights: {lights.name()} - created")
            print(
                f"* Lights Definition: {lights_definition.name()} - assigned")
            # Assign it to the corresponding space type - In this case, space type is assigned to People
            lights.setSpaceType(
                osm_model.getSpaceTypeByName(row['Name']).get())
            print(f"* Lights: {lights.name()} - assigned")

    # Electric Equipment & Electric Equipment Definition
    for index, row in all_space_types_df.iterrows():
        elect_eqp_new_name = f"{row['Name']} Electric Equipment"
        elect_eqp_definition_new_name = f"{row['Name']} Electric Equipment Definition"
        # Create a new object and assig it
        if (create_if_none and row['Electric Equipment Load Name'] == None) or (row['Electric Equipment Load Name'] != None and row['Electric Equipment Load Name'] != elect_eqp_new_name):
            # Create ElectricEquipment:Definition object first
            elect_eqp_definition = openstudio.model.ElectricEquipmentDefinition(
                osm_model)
            elect_eqp_definition.setName(elect_eqp_definition_new_name)
            elect_eqp_definition.setDesignLevel(0)
            print(
                f"* ElectricEquipment Definition: {elect_eqp_definition.name()} - created")
            # Create ElectricEquipment object from ElectricEquipment:Definition
            elect_eqp = openstudio.model.ElectricEquipment(
                elect_eqp_definition)
            elect_eqp.setName(elect_eqp_new_name)
            print(f"* Electric Equipment: {elect_eqp.name()} - created")
            print(
                f"* Electric Equipment Definition: {elect_eqp_definition.name()} - assigned")
            # Assign it to the corresponding space type - In this case, space type is assigned to People
            elect_eqp.setSpaceType(
                osm_model.getSpaceTypeByName(row['Name']).get())
            print(f"* Electric Equipment: {elect_eqp.name()} - assigned")

    # SCHEDULES
    # ----------

    # Get all space types (again)
    all_space_types_df = get_all_space_types_as_dataframe(osm_model)
    all_space_types_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    # People Number Of People Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Number Of People Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['People Number Of People Schedule'] == None) or (row['People Number Of People Schedule'] != None and row['People Number Of People Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setNumberofPeopleSchedule(schdle_ruleset.get())
    # People Activity Level Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} People Activity Level Schedule"
        schdle_ruleset_type = 'ActivityLevel'
        # Create a new object and assig it
        if (create_if_none and row['People Activity Level Schedule'] == None) or (row['People Activity Level Schedule'] != None and row['People Activity Level Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setPeopleActivityLevelSchedule(schdle_ruleset.get())
    # Lighting Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Lighting Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['Lighting Schedule'] == None) or (row['Lighting Schedule'] != None and row['Lighting Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(
                row['Default Schedule Set']).get().setLightingSchedule(schdle_ruleset.get())

    # Electric Equipment Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Electric Equipment Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['Electric Equipment Schedule'] == None) or (row['Electric Equipment Schedule'] != None and row['Electric Equipment Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setElectricEquipmentSchedule(schdle_ruleset.get())

    # Infiltration Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Infiltration Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['Infiltration Schedule'] == None) or (row['Infiltration Schedule'] != None and row['Infiltration Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setInfiltrationSchedule(schdle_ruleset.get())
    
    return osm_model
