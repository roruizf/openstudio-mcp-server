import openstudio
import pandas as pd
import numpy as np
import datetime
import calendar


def get_all_default_schedule_set_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all default schedule set objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all default schedule set objects.
    """

    # OS:DefaultScheduleSet
    # Get all schedule set in the OpenStudio model.
    all_default_schedule_set_objects = osm_model.getDefaultScheduleSets()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_default_schedule_set_objects],
        'Name': [x.name().get() for x in all_default_schedule_set_objects],
        'Hours of Operation Schedule Name': [x.hoursofOperationSchedule().get().nameString() if not x.hoursofOperationSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Number of People Schedule Name': [x.numberofPeopleSchedule().get().nameString() if not x.numberofPeopleSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'People Activity Level Schedule Name': [x.peopleActivityLevelSchedule().get().nameString() if not x.peopleActivityLevelSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Lighting Schedule Name': [x.lightingSchedule().get().nameString() if not x.lightingSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Electric Equipment Schedule Name': [x.electricEquipmentSchedule().get().nameString() if not x.electricEquipmentSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Gas Equipment Schedule Name': [x.gasEquipmentSchedule().get().nameString() if not x.gasEquipmentSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Hot Water Equipment Schedule Name': [x.hotWaterEquipmentSchedule().get().nameString() if not x.hotWaterEquipmentSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Infiltration Schedule Name': [x.infiltrationSchedule().get().nameString() if not x.infiltrationSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Steam Equipment Schedule Name': [x.steamEquipmentSchedule().get().nameString() if not x.steamEquipmentSchedule().isNull() else None for x in all_default_schedule_set_objects],
        'Other Equipment Schedule Name': [x.otherEquipmentSchedule().get().nameString() if not x.otherEquipmentSchedule().isNull() else None for x in all_default_schedule_set_objects]
    }

    # Create a DataFrame of all schedule ruleset objects.
    all_default_schedule_sets_df = pd.DataFrame(columns=object_attr.keys())

    for key in object_attr.keys():
        all_default_schedule_sets_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_default_schedule_sets_df = all_default_schedule_sets_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_default_schedule_sets_df.shape[0]} default schedule sets objects")

    return all_default_schedule_sets_df


def get_all_schedule_ruleset_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:Schedule:Ruleset
    # Get all schedule ruleset in the OpenStudio model.
    all_schedule_ruleset_objects = osm_model.getScheduleRulesets()
    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_schedule_ruleset_objects],
        'Name': [x.name().get() for x in all_schedule_ruleset_objects],
        'Schedule Type Limits Name': [x.scheduleTypeLimits().get().nameString() if not x.scheduleTypeLimits().isNull() else None for x in all_schedule_ruleset_objects],
        'Default Day Schedule Name': [x.defaultDaySchedule().nameString() for x in all_schedule_ruleset_objects],
        'Summer Design Day Schedule Name': [x.summerDesignDaySchedule().nameString() for x in all_schedule_ruleset_objects],
        'Winter Design Day Schedule Name': [x.winterDesignDaySchedule().nameString() for x in all_schedule_ruleset_objects]
    }
    # Create a DataFrame of all schedule ruleset objects.
    all_schedule_ruleset_objects_df = pd.DataFrame(columns=object_attr.keys())

    for key in object_attr.keys():
        all_schedule_ruleset_objects_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_schedule_ruleset_objects_df = all_schedule_ruleset_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_schedule_ruleset_objects_df.shape[0]} schedule ruleset objects")

    return all_schedule_ruleset_objects_df


def get_all_schedule_rule_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:Schedule:Rule
    # Get all schedule ruleset in the OpenStudio model.
    all_schedule_rule_objects = osm_model.getScheduleRules()
    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_schedule_rule_objects],
        'Name': [x.name().get() for x in all_schedule_rule_objects],
        'Schedule Ruleset Name': [x.scheduleRuleset().nameString() for x in all_schedule_rule_objects],
        'Rule Order': [x.ruleIndex() for x in all_schedule_rule_objects],
        'Day Schedule Name': [x.daySchedule().nameString() for x in all_schedule_rule_objects],
        'Apply Sunday': [x.applySunday() for x in all_schedule_rule_objects],
        'Apply Monday': [x.applyMonday() for x in all_schedule_rule_objects],
        'Apply Tuesday': [x.applyTuesday() for x in all_schedule_rule_objects],
        'Apply Wednesday': [x.applyWednesday() for x in all_schedule_rule_objects],
        'Apply Thursday': [x.applyThursday() for x in all_schedule_rule_objects],
        'Apply Friday': [x.applyFriday() for x in all_schedule_rule_objects],
        'Apply Saturday': [x.applySaturday() for x in all_schedule_rule_objects],
        'Date Specification Type': [x.dateSpecificationType() for x in all_schedule_rule_objects],
        'Start Month': [x.startDate().get().monthOfYear().value() if not x.startDate().isNull() else None for x in all_schedule_rule_objects],
        'Start Day': [x.startDate().get().dayOfMonth() if not x.startDate().isNull() else None for x in all_schedule_rule_objects],
        'End Month': [x.endDate().get().monthOfYear().value() if not x.endDate().isNull() else None for x in all_schedule_rule_objects],
        'End Day': [x.endDate().get().dayOfMonth() if not x.endDate().isNull() else None for x in all_schedule_rule_objects]
    }
    # Create a DataFrame of all schedule ruleset objects.
    all_schedule_rule_objects_df = pd.DataFrame(columns=object_attr.keys())

    for key in object_attr.keys():
        all_schedule_rule_objects_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_schedule_rule_objects_df = all_schedule_rule_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_schedule_rule_objects_df.shape[0]} schedule rule objects")

    return all_schedule_rule_objects_df


def get_all_schedule_day_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:Schedule:Day
    # Get all schedule ruleset in the OpenStudio model.
    all_schedule_day_objects = osm_model.getScheduleDays()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_schedule_day_objects],
        'Name': [x.name().get() for x in all_schedule_day_objects],
        'Schedule Type Limits Name': [x.scheduleTypeLimits().get().nameString() if not x.scheduleTypeLimits().isNull() else None for x in all_schedule_day_objects],
        'Interpolate to Timestep': [x.interpolatetoTimestep() for x in all_schedule_day_objects],
        'Hour':  [tuple(item.hours() for item in x.times()) for x in all_schedule_day_objects],
        'Minute':  [tuple(item.minutes() for item in x.times()) for x in all_schedule_day_objects],
        'Values': [x.values() for x in all_schedule_day_objects]

    }
    # Create a DataFrame of all schedule day objects.
    all_schedule_day_objects_df = pd.DataFrame(columns=object_attr.keys())

    for key in object_attr.keys():
        all_schedule_day_objects_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_schedule_day_objects_df = all_schedule_day_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_schedule_day_objects_df.shape[0]} schedule day objects")

    return all_schedule_day_objects_df


def get_all_schedule_type_limit_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:Schedule:Day
    # Get all schedule ruleset in the OpenStudio model.
    all_schedule_type_limit_objects = osm_model.getScheduleTypeLimitss()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_schedule_type_limit_objects],
        'Name': [x.name().get() for x in all_schedule_type_limit_objects],
        'Lower Limit Value': [x.lowerLimitValue().get() if not x.lowerLimitValue().isNull() else None for x in all_schedule_type_limit_objects],
        'Upper Limit Value': [x.upperLimitValue().get() if not x.upperLimitValue().isNull() else None for x in all_schedule_type_limit_objects],
        'Numeric Type': [x.numericType().get() if not x.numericType().isNull() else None for x in all_schedule_type_limit_objects]
        # 'Interpolate to Timestep': [x.interpolatetoTimestep() for x in all_schedule_type_limit_objects],
        # 'Hour':  [tuple(item.hours() for item in x.times()) for x in all_schedule_type_limit_objects],
        # 'Minute':  [tuple(item.minutes() for item in x.times()) for x in all_schedule_type_limit_objects],
        # 'Values': [x.values() for x in all_schedule_type_limit_objects]

    }
    # Create a DataFrame of all schedule day objects.
    all_schedule_type_limit_objects_df = pd.DataFrame(
        columns=object_attr.keys())

    for key in object_attr.keys():
        all_schedule_type_limit_objects_df[key] = object_attr[key]

    # Replace NaN values with None
    all_schedule_type_limit_objects_df = all_schedule_type_limit_objects_df.replace(
        np.nan, None)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_schedule_type_limit_objects_df = all_schedule_type_limit_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_schedule_type_limit_objects_df.shape[0]} schedule type limit objects")

    return all_schedule_type_limit_objects_df


def get_all_default_schedule_set_components_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    
    """
    Retrieves all default schedule set components from an OpenStudio model and formats them into a DataFrame.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model from which to extract the components. 

    Returns:
        pd.DataFrame: A DataFrame containing all default schedule set components organized by type.
    """
    all_default_schedule_set_df = get_all_default_schedule_set_objects_as_dataframe(osm_model)
    columns_to_stack = all_default_schedule_set_df.columns[~all_default_schedule_set_df.columns.isin(['Handle', 'Name'])].tolist()
    default_schedule_ruleset_df = all_default_schedule_set_df.melt(id_vars=['Handle', 'Name'], value_vars=columns_to_stack, var_name='Schedule Ruleset Type', value_name='Schedule Name').sort_values(by=['Handle', 'Name']).drop(columns=['Handle'])
    default_schedule_ruleset_df = default_schedule_ruleset_df.rename(columns={'Name': 'Default Schedule Set Name', 'Schedule Name': 'Schedule Ruleset Name'})
    default_schedule_ruleset_df['Schedule Ruleset Type'] = default_schedule_ruleset_df['Schedule Ruleset Type'].str.replace('Name', '').str.strip()
    default_schedule_ruleset_df = default_schedule_ruleset_df.dropna().reset_index(drop=True)

    all_schedule_ruleset_objects_df = get_all_schedule_ruleset_objects_as_dataframe(osm_model)
    default_schedule_ruleset_df = pd.merge(default_schedule_ruleset_df, all_schedule_ruleset_objects_df, left_on='Schedule Ruleset Name', right_on='Name', how='left')
    default_schedule_ruleset_df = default_schedule_ruleset_df.drop(columns=['Handle', 'Name'])
    default_schedule_ruleset_df = default_schedule_ruleset_df.replace(np.nan, None)
    columns_to_stack = default_schedule_ruleset_df.columns[~default_schedule_ruleset_df.columns.isin(['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name'])].tolist()
    default_schedule_day_df = default_schedule_ruleset_df.melt(id_vars=['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name'], value_vars=columns_to_stack,
                                                                var_name='Schedule Day Type', value_name='Schedule Day Name').sort_values(by=['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name']).reset_index(drop=True)
    default_schedule_day_df['Schedule Day Type'] = default_schedule_day_df['Schedule Day Type'].str.replace('Name', '').str.strip().reset_index(drop=True)

    all_schedule_day_objects_df = get_all_schedule_day_objects_as_dataframe(osm_model)
    all_schedule_rule_objects_df = get_all_schedule_rule_objects_as_dataframe(osm_model)
    default_schedule_rule_objects_df = all_schedule_rule_objects_df[all_schedule_rule_objects_df['Schedule Ruleset Name'].isin(default_schedule_day_df['Schedule Ruleset Name'].unique())]

    # Stacking priority day schedules and rules
    default_schedule_day_df['Schedule Rule Name'] = np.nan
    default_schedule_day_df['Schedule Rule Order'] = np.nan
    default_schedule_day_df
    for index, row in default_schedule_rule_objects_df.iterrows():
        schedule_ruleset_name = row['Schedule Ruleset Name']
        default_schedule_day_df_i = pd.DataFrame()
        default_schedule_day_df_i = default_schedule_day_df[default_schedule_day_df['Schedule Ruleset Name'] == schedule_ruleset_name]
        default_schedule_day_df_i = default_schedule_day_df_i.drop_duplicates(['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name',
                                                                                'Schedule Type Limits Name'], keep='first')
        default_schedule_day_df_i['Schedule Day Name'] = row['Day Schedule Name']
        default_schedule_day_df_i['Schedule Day Type'] = 'Rule Day Schedule'
        default_schedule_day_df_i['Schedule Rule Name'] = row['Name']
        default_schedule_day_df_i['Schedule Rule Order'] = str(row['Rule Order'])
        
        default_schedule_day_df = pd.concat([default_schedule_day_df, default_schedule_day_df_i], ignore_index=True)
        default_schedule_day_df = default_schedule_day_df.replace(np.nan, None)

    default_schedule_day_df = default_schedule_day_df.sort_values(by=['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name']).reset_index(drop=True)

    return default_schedule_day_df


def get_schedule_type_limits_parms(schedule_type_limits_name: str) -> dict:
    """
    Retrieve parameters for a given schedule type limits name.

    Parameters:
    - schedule_type_limits_name (str): Name of the schedule type limits.

    Returns:
    - dict: Parameters associated with the given schedule type limits name.
    """

    # Default parameters for different schedule type limits
    all_possible_schedule_type_limits_parms = {
        'ActivityLevel': {
            'Lower Limit Value': 0,
            'Upper Limit Value': None,
            'Numeric Type': 'Continuous',
            'Unit Type': 'ActivityLevel'
        },
        'InternalGains': {
            'Lower Limit Value': 0,
            'Upper Limit Value': 1,
            'Numeric Type': 'Continuous',
            'Unit Type': 'Dimensionless'
        },
        'IndoorSetpoint': {
            'Lower Limit Value': None,
            'Upper Limit Value': None,
            'Numeric Type': 'Continuous',
            'Unit Type': 'Temperature'
        }
    }

    # Check if the provided schedule type limits name exists in the dictionary
    if schedule_type_limits_name not in all_possible_schedule_type_limits_parms:
        raise KeyError(
            f"The key '{schedule_type_limits_name}' needs to be defined in the dictionary. Check function 'get_schedule_type_limits_parms' ")
    else:
        # Return parameters associated with the provided schedule type limits name
        return all_possible_schedule_type_limits_parms[schedule_type_limits_name]


def create_new_schedule_type_limits(
    osm_model: openstudio.model.Model,
    schedule_type_limits__name: str
) -> None:
    """
    Create a new ScheduleTypeLimits object and set its properties.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio model to which the ScheduleTypeLimits will be added.
    - schedule_type_limits_name (str): Name of the ScheduleTypeLimits.

    Note:
    This function does not return any value. It creates and configures the ScheduleTypeLimits in-place.
    """
    # Define sets of possible values
    POSSIBLE_NUMERIC_TYPES = {'Continuous', 'Discrete', 'OnOff', 'Control'}
    POSSIBLE_UNIT_TYPES = {'Dimensionless',
                           'Temperature', 'Power', 'Other', 'ActivityLevel'}

    # Load Schedule Type Limits parameters
    schedule_type_limits_parms = get_schedule_type_limits_parms(
        schedule_type_limits__name)
    lower_limit_value = schedule_type_limits_parms['Lower Limit Value']
    upper_limit_value = schedule_type_limits_parms['Upper Limit Value']
    numeric_type = schedule_type_limits_parms['Numeric Type']
    unit_type = schedule_type_limits_parms['Unit Type']

    # Check if input values are valid
    if numeric_type not in POSSIBLE_NUMERIC_TYPES:
        raise ValueError(
            f"Invalid numeric_type. Possible values are {POSSIBLE_NUMERIC_TYPES}")

    if unit_type not in POSSIBLE_UNIT_TYPES:
        raise ValueError(
            f"Invalid unit_type. Possible values are {POSSIBLE_UNIT_TYPES}")

    # Create ScheduleTypeLimits object
    schedule_type_limits = openstudio.model.ScheduleTypeLimits(osm_model)

    # Set Name
    schedule_type_limits.setName(schedule_type_limits__name)

    # Set lower_limit_value if not None
    if lower_limit_value is not None:
        schedule_type_limits.setLowerLimitValue(lower_limit_value)

    # Set upper_limit_value if not None
    if upper_limit_value is not None:
        schedule_type_limits.setUpperLimitValue(upper_limit_value)
    # Set Numeric Type
    schedule_type_limits.setNumericType(numeric_type)
    # Set £UNit Type
    schedule_type_limits.setUnitType(unit_type)


def create_new_default_schedule_ruleset(osm_model: openstudio.model.Model,
                                        schedule_ruleset__name: str,
                                        schedule_type_limits__name: str
                                        ) -> None:
    """
    Create a new ScheduleRuleset object with default parameters.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio model to which the ScheduleRuleset will be added.
    - schedule_ruleset__name (str): Name of the ScheduleRuleset.
    - schedule_type_limits__name (str): Name of the ScheduleTypeLimits associated with the ScheduleRuleset.
    """

    # Create Schedule RuleSet
    # ------------------------
    schedule_ruleset = openstudio.model.ScheduleRuleset(osm_model)
    # Set Schedule RuleSet Name
    schedule_ruleset.setName(schedule_ruleset__name)
    # Set Schedule Default Day Schedule Day (this is automatically created when RuleSet is created)
    schedule_ruleset.defaultDaySchedule().setName(
        f"{schedule_ruleset__name} Default")

    # Assing Schedule Type Limits
    # ----------------------------
    type_limit__name = schedule_type_limits__name

    # Create ScheduleTypeLimits if not already present
    if osm_model.getScheduleTypeLimitsByName(type_limit__name).isNull():
        create_new_schedule_type_limits(osm_model, type_limit__name)

    # Load Schedule Type Limits
    schedule_type_limits = osm_model.getScheduleTypeLimitsByName(
        type_limit__name).get()

    # Set Schedule Type Limits
    schedule_ruleset.setScheduleTypeLimits(schedule_type_limits)

    # Set Default Schedule RulseSet Parameters: Winter and Summer Days

    # Default parameters
    default_schedule_ruleset_params = {
        'ActivityLevel': {
            'Design Day': {
                'Winter Design Day Default Value': 132,
                'Summer Design Day Default Value': 132,
            }
        },
        'InternalGains': {
            'Design Day': {
                'Winter Design Day Default Value': 0,
                'Summer Design Day Default Value': 1,
            }
        },
        'IndoorSetpoint': {
            'Design Day': {
                'Winter Design Day Default Value': 21,
                'Summer Design Day Default Value': 24,
            }
        }}

    # Configure Design Days if provided
    design_days_params = default_schedule_ruleset_params[schedule_type_limits__name]['Design Day']

    if design_days_params is not None:

        # Winter Design Day
        # -----------------
        winter_design_day = openstudio.model.ScheduleDay(osm_model)
        winter_design_day.setName(
            f"{schedule_ruleset.name().get()} Winter Design Day")
        winter_design_day.setScheduleTypeLimits(schedule_type_limits)
        default_value = design_days_params['Winter Design Day Default Value']
        untilTime = winter_design_day.times()[0]
        winter_design_day.addValue(untilTime, default_value)
        # Assign Winter Schedule Day to Schedule RulseSet
        schedule_ruleset.setWinterDesignDaySchedule(winter_design_day)

        # Summer Design Day
        # -----------------
        summer_design_day = openstudio.model.ScheduleDay(osm_model)
        summer_design_day.setName(
            f"{schedule_ruleset.name().get()} Summer Design Day")
        summer_design_day.setScheduleTypeLimits(schedule_type_limits)
        untilTime = summer_design_day.times()[0]
        default_value = design_days_params['Summer Design Day Default Value']
        summer_design_day.addValue(untilTime, default_value)
        # Assign Summer Schedule Day to Schedule RulseSet
        schedule_ruleset.setSummerDesignDaySchedule(summer_design_day)


def create_new_schedule_ruleset(
    osm_model: openstudio.model.Model,
    schdle_ruleset_name: str,
    schdle_ruleset_type: str
) -> None:
    """
    Create a new ScheduleRuleset object and configure its properties based on provided parameters.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio model to which the ScheduleRuleset will be added.
    - schdle_ruleset_name (str): Name of the ScheduleRuleset.
    - schdle_ruleset_type (str): Type of the ScheduleRuleset ('Internal Gains', 'Indoor Setpoint', etc.).
    """
    # Default parameters
    schdle_ruleset_params = {
        'ActivityLevel': {
            'ScheduleTypeLimits': {
                'Lower Limit Value': 0,
                'Upper Limit Value': None,
                'Numeric Type': 'Continuous',
                'Unit Type': 'ActivityLevel'
            },
            'Design Day': {
                'Winter Design Day Default Value': 132,
                'Summer Design Day Default Value': 132,
            }
        },
        'InternalGains': {
            'ScheduleTypeLimits': {
                'Lower Limit Value': 0,
                'Upper Limit Value': 1,
                'Numeric Type': 'Continuous',
                'Unit Type': 'Dimensionless'
            },
            'Design Day': {
                'Winter Design Day Default Value': 0,
                'Summer Design Day Default Value': 1,
            }
        },
        'IndoorSetpoint': {
            'ScheduleTypeLimits': {
                'Lower Limit Value': None,
                'Upper Limit Value': None,
                'Numeric Type': 'Continuous',
                'Unit Type': 'Temperature'
            },
            'Design Day': None
        }
    }

    # Check if schdle_ruleset_type is in schdle_ruleset_params
    if schdle_ruleset_type not in schdle_ruleset_params:
        raise ValueError(
            f"Invalid schdle_ruleset_type. Possible values are {list(schdle_ruleset_params.keys())}")

    # Possible parameters
    type_limit_params = schdle_ruleset_params[schdle_ruleset_type]['ScheduleTypeLimits']
    type_limit_name = schdle_ruleset_type
    type_limit_lower_value = type_limit_params['Lower Limit Value']
    type_limit_upper_value = type_limit_params['Upper Limit Value']
    type_limit_numeric_type = type_limit_params['Numeric Type']
    type_limit_unit_type = type_limit_params['Unit Type']

    # Create ScheduleTypeLimits if not already present
    if osm_model.getScheduleTypeLimitsByName(type_limit_name).isNull():
        create_new_schedule_type_limits(osm_model, type_limit_name)
        # create_new_schedule_type_limits(osm_model, type_limit_name, type_limit_lower_value,
        #                                 type_limit_upper_value, type_limit_numeric_type, type_limit_unit_type)

    schdle_type_limit = osm_model.getScheduleTypeLimitsByName(
        type_limit_name).get()
    schdle_ruleset = openstudio.model.ScheduleRuleset(osm_model)
    schdle_ruleset.setName(schdle_ruleset_name)
    schdle_ruleset.defaultDaySchedule().setName(
        f"{schdle_ruleset_name} Default")
    schdle_ruleset.setScheduleTypeLimits(schdle_type_limit)

    # Configure Design Days if provided
    design_days_params = schdle_ruleset_params[schdle_ruleset_type]['Design Day']
    if design_days_params is not None:
        # Winter Design Day
        winter_design_day_default_value = design_days_params['Winter Design Day Default Value']
        winter_design_day = openstudio.model.ScheduleDay(osm_model)
        winter_design_day.setName(
            f"{schdle_ruleset.name().get()} Winter Design Day")
        winter_design_day.setScheduleTypeLimits(schdle_type_limit)
        winter_design_day.setString(6, str(winter_design_day_default_value))
        schdle_ruleset.setWinterDesignDaySchedule(winter_design_day)

        # Summer Design Day
        summer_design_day_default_value = design_days_params['Summer Design Day Default Value']
        summer_design_day = openstudio.model.ScheduleDay(osm_model)
        summer_design_day.setName(
            f"{schdle_ruleset.name().get()} Summer Design Day")
        summer_design_day.setScheduleTypeLimits(schdle_type_limit)
        summer_design_day.setString(6, str(summer_design_day_default_value))
        schdle_ruleset.setSummerDesignDaySchedule(summer_design_day)


def create_rule_schedule_day(osm_model: openstudio.model.Model,
                             schedule_rule_set__name: str,
                             schedule_day__hours: tuple,
                             schedule_day__minutes: tuple,
                             schedule_day__values: tuple,
                             apply_weekdays: dict,
                             start_date_strftime: str = '2007-01-01',
                             end_date_strftime: str = '2007-12-30'
                             ) -> None:
    """
    Create a new ScheduleDay and ScheduleRule and assign weekdays, start date, and end date.

    Parameters:
    - schedule_rule_set__name (str): Name of the schedule rule set.
    - schedule_day__hours (tuple): Tuple of hours for schedule day values.
    - schedule_day__minutes (tuple): Tuple of minutes for schedule day values.
    - schedule_day__values (tuple): Tuple of values for schedule day.
    - apply_weekdays (dict): Dictionary indicating which weekdays the schedule applies to.
    - start_date_strftime (str): Start date in strftime format (default is '2007-01-01').
    - end_date_strftime (str): End date in strftime format (default is '2007-12-30').

    Note:
    This function does not return any value. It creates and configures ScheduleDay and ScheduleRule objects.
    """

    # Get target schedule ruleset
    schedule_ruleset = osm_model.getScheduleRulesetByName(
        schedule_rule_set__name).get()

    # Create new Schedule Day
    schedule_day = openstudio.model.ScheduleDay(osm_model)

    # Set type limit: if ruleset is defined then type limit is too
    schedule_type_limit_name = schedule_ruleset.scheduleTypeLimits().get().nameString()
    schedule_type_limit = osm_model.getScheduleTypeLimitsByName(
        schedule_type_limit_name).get()
    schedule_day.setScheduleTypeLimits(schedule_type_limit)
    schedule_day_name = schedule_rule_set__name.replace(
        'Schedule', 'Rule Day Schedule')
    schedule_day.setName(schedule_day_name)

    # Add values to the ScheduleDay
    for hour, minute, value in zip(schedule_day__hours, schedule_day__minutes, schedule_day__values):
        until_time = openstudio.Time(0, int(hour), int(minute))
        schedule_day.addValue(until_time, value)

    # Create Schedule Rule
    schedule_rule = openstudio.model.ScheduleRule(
        schedule_ruleset, schedule_day)
    schedule_rule_name = schedule_rule_set__name.replace('Schedule', 'Rule')
    schedule_rule.setName(schedule_rule_name)

    # Assign weekdays
    if apply_weekdays.get('Monday', None):
        schedule_rule.setApplyMonday(apply_weekdays['Monday'])
    if apply_weekdays.get('Tuesday', None):
        schedule_rule.setApplyTuesday(apply_weekdays['Tuesday'])
    if apply_weekdays.get('Wednesday', None):
        schedule_rule.setApplyWednesday(apply_weekdays['Wednesday'])
    if apply_weekdays.get('Thursday', None):
        schedule_rule.setApplyThursday(apply_weekdays['Thursday'])
    if apply_weekdays.get('Friday', None):
        schedule_rule.setApplyFriday(apply_weekdays['Friday'])
    if apply_weekdays.get('Saturday', None):
        schedule_rule.setApplySaturday(apply_weekdays['Saturday'])
    if apply_weekdays.get('Sunday', None):
        schedule_rule.setApplySunday(apply_weekdays['Sunday'])

    # Assign start and end date
    start_date = openstudio.Date(start_date_strftime)
    end_date = openstudio.Date(end_date_strftime)
    schedule_rule.setStartDate(start_date)
    schedule_rule.setEndDate(end_date)


def calculate_equivalent_full_hours(hours: tuple, minutes: tuple, values: tuple, full_load_value: float = 1) -> float:
    """
    Calculates equivalent full load hours based on hourly values.

    Args:
        hours (tuple): Tuple of hours representing the schedule (24-hour format).
        minutes (tuple): Tuple of minutes corresponding to each hour in the schedule.
        values (tuple): Tuple of values as fractions of full load for each corresponding hour.
        full_load_value (float, optional): The full load value to scale the output. Defaults to 1.

    Returns:
        float: Equivalent full hours calculated from input values and durations.
    """
    # Convert input tuples to NumPy arrays for efficient calculations
    hours = np.array(list(hours)[:-1] + [24])
    minutes = np.array(minutes)
    values = np.array(values)

    # Calculate the current time in hours
    current_time_in_hours = hours + (minutes / 60.0)

    # Calculate the time differences
    time_differences = np.diff(np.insert(current_time_in_hours, 0, 0))  # Insert 0 for the start of the day

    # Calculate total time and equivalent full load hours
    total_time = np.sum(time_differences)  # Should always be 24 hours
    equivalent_full_hours = np.sum(values * time_differences)

    return equivalent_full_hours  # Return the equivalent full hours

def weekday_count(start_date: str, end_date: str) -> dict:
    """
    Counts occurrences of each weekday in the given date range.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary with weekdays as keys and their counts as values.
    """
    # Convert string dates to datetime objects
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize a dictionary to hold counts of each weekday
    number_of_days = {day: 0 for day in calendar.day_name}

    # Iterate through the range of dates
    for i in range((end_date - start_date).days + 1):  # Include the end date
        current_date = start_date + datetime.timedelta(days=i)
        day_name = calendar.day_name[current_date.weekday()]
        number_of_days[day_name] += 1

    return number_of_days


def convert_schedule_to_daily_profile(hours, minutes, values, timestep=1):
    """
    Convert a schedule defined by hours, minutes, and values into a daily profile.

    Args:
        hours: A tuple containing hour values.
        minutes: A tuple containing minute values.
        values: A tuple containing corresponding values.
        timestep: The time interval in hours for the daily time profile (default is 1 hour).

    Returns:
        A tuple containing two lists:
            - daily_times_profile: A list of daily time values in hours.
            - daily_values_profile: A list of daily values corresponding to daily times.
    """
    # Convert input tuples to NumPy arrays for efficient calculations
    hours = np.array(list(hours)[:-1] + [24])[::-1]  # Add 24 as the last hour
    minutes = np.array(minutes)[::-1]  # Convert minutes to NumPy array
    values = np.array(values)[::-1]  # Convert values to NumPy array

    # Calculate the current time in hours
    time_in_hours = hours + (minutes / 60.0)

    # Create daily time array with the specified timestep
    daily_time = np.arange(0, 24, timestep)  # Use the provided timestep

    # Initialize daily_values with the first value
    daily_values = np.array([values[0]] * len(daily_time))

    # Assign values based on time_in_hours
    for i in range(len(time_in_hours)):
        index = np.where(daily_time < time_in_hours[i])[0]
        daily_values[index] = values[i]

    # Convert the NumPy arrays to lists for the output
    daily_times_profile = daily_time.tolist()
    daily_values_profile = daily_values.tolist()

    return daily_times_profile, daily_values_profile