import openstudio
import pandas as pd
import numpy as np


def get_all_building_stories_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all building stories from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all building stories.
    """

    # Get all building storeys in the OpenStudio model.
    all_building_stories = osm_model.getBuildingStorys()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_building_stories],
        'Name': [x.name().get() for x in all_building_stories],
        'Nominal Z Coordinate {m}': [x.nominalZCoordinate().get() if not x.nominalZCoordinate().isNull() else None for x in all_building_stories],
        'Nominal Floor to Floor Height {m}': [x.nominalFloortoFloorHeight().get() if not x.nominalFloortoFloorHeight().isNull() else None for x in all_building_stories],
        'Default Construction Set Name': [x.defaultConstructionSet().get().name().get() if not x.defaultConstructionSet().isNull() else None for x in all_building_stories],
        'Default Schedule Set Name': [x.defaultScheduleSet().get().name().get() if not x.defaultScheduleSet().isNull() else None for x in all_building_stories],
        'Group Rendering Name': [x.renderingColor().get().name().get() if not x.renderingColor().isNull() else None for x in all_building_stories],
        'Nominal Floor to Ceiling Height {m}': [x.nominalFloortoCeilingHeight().get() if not x.nominalFloortoCeilingHeight().isNull() else None for x in all_building_stories]
    }

    # Create a DataFrame of building.
    all_building_stories_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_building_stories_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_building_stories_df = all_building_stories_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    return all_building_stories_df


def create_new_building_stories_objects(osm_model: openstudio.model.Model, building_stories_to_create_df: pd.DataFrame) -> None:
    """
    Create new building stories components based on data from a New Objects DataFrame.

    Parameters:
    - osm_model: The OpenStudio Model object.
    - building_stories_to_create_df: DataFrame containing data for new building story components.

    Returns:
    - None
    """
    building_stories_to_create_df = building_stories_to_create_df.replace(
        np.nan, None)

    for _, row in building_stories_to_create_df.iterrows():
        new_story = openstudio.model.BuildingStory(osm_model)
        new_story.setName(row['Name'])

        # Setting attributes if defined in building_stories_to_create_df

        # Nominal Z Coordinate {m}
        if row['Nominal Z Coordinate {m}'] is not None:
            new_story.setNominalZCoordinate(row['Nominal Z Coordinate {m}'])

        # Nominal Floor to Floor Height {m}
        if row['Nominal Floor to Floor Height {m}'] is not None:
            new_story.setNominalFloortoFloorHeight(
                row['Nominal Floor to Floor Height {m}'])

        # Default Construction Set Name
        if row['Default Construction Set Name'] is not None:
            new_construction_set = openstudio.model.DefaultConstructionSet(
                osm_model)
            new_story.setDefaultConstructionSet(new_construction_set)

        # Default Schedule Set Name
        if row['Default Schedule Set Name'] is not None:
            new_schedule_set = openstudio.model.DefaultScheduleSet(osm_model)
            new_story.setDefaultScheduleSet(new_schedule_set)

        # Group Rendering Name
        if row['Group Rendering Name'] is not None:
            if osm_model.getRenderingColorByName(row['Group Rendering Name']).isNull():
                rendering_color = openstudio.model.RenderingColor(osm_model)
            else:
                rendering_color = osm_model.getRenderingColorByName(
                    row['Group Rendering Name']).get()

            rendering_color.setName(row['Group Rendering Name'])
            new_story.setRenderingColor(rendering_color)

        # Nominal Floor to Ceiling Height {m}
        if row['Nominal Floor to Ceiling Height {m}'] is not None:
            new_story.setNominalFloortoCeilingHeight(
                row['Nominal Floor to Ceiling Height {m}'])

    print(
        f"{building_stories_to_create_df.shape[0]} new building story objects created")


def update_building_stories_objects(osm_model, building_stories_to_update_df):

    for _, row in building_stories_to_update_df.iterrows():
        story = osm_model.getBuildingStory(row['Handle'])

        # Nominal Z Coordinate {m}
        if row['Nominal Z Coordinate {m}'] is not None:
            story.get().setNominalZCoordinate(row['Nominal Z Coordinate {m}'])

        # Nominal Floor to Floor Height {m}
        if row['Nominal Floor to Floor Height {m}'] is not None:
            story.get().setNominalFloortoFloorHeight(
                row['Nominal Floor to Floor Height {m}'])

        # Default Construction Set Name
        if row['Default Construction Set Name'] is not None:
            pass

        # Set new name
        if row['Name'] is not None:
            pass

        # Default Schedule Set Name
        if row['Default Schedule Set Name'] is not None:
            pass

        # Group Rendering Name
        if row['Group Rendering Name'] is not None:
            pass

        # Nominal Floor to Ceiling Height {m}
        if row['Nominal Floor to Ceiling Height {m}'] is not None:
            story.get().setNominalFloortoCeilingHeight(
                row['Nominal Floor to Ceiling Height {m}'])


def set_stories_to_spaces(osm_model: openstudio.model.Model, space_story_dict_list: list) -> None:
    """
    Assigns building stories to spaces in the given OpenStudio model.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model containing spaces.
        space_story_dict_list (list): A list of dictionaries where each dictionary contains.
            'Handle' (str) - The unique identifier for a space.
            'Story' (str) - The name of the building story to assign.

    Returns:
        None: This function does not return a value.
    """
    # Convert the list of dictionaries to a DataFrame for easier manipulation.
    space_story_df = pd.DataFrame(space_story_dict_list)

    # Iterate over the DataFrame rows to set building stories for each space.
    for index, row in space_story_df.iterrows():
        osm_model.getSpace(row['Handle']).get().setBuildingStory(
            osm_model.getBuildingStoryByName(row['Story']).get())
