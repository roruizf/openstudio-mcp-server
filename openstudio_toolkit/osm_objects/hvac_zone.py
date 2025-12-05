import openstudio
import pandas as pd

#--
#-- OS:ZoneHVAC:EquipmentList
#--

def get_all_zone_hvac_equipment_list_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all zone HVAC Equipment List from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """
    all_zone_hvac_equipment_lists = osm_model.getZoneHVACEquipmentLists()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_zone_hvac_equipment_lists],
        'Name': [x.name().get() for x in all_zone_hvac_equipment_lists],
        'Thermal Zone': [x.thermalZone().name().get() for x in all_zone_hvac_equipment_lists],
        'Load Distribution Scheme': [x.loadDistributionScheme() for x in all_zone_hvac_equipment_lists]
        }

    # Create a DataFrame of all thermal zones.
    all_zone_hvac_equipment_lists_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_zone_hvac_equipment_lists_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_zone_hvac_equipment_lists_df = all_zone_hvac_equipment_lists_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    # Get maximum number of zoneHVAC equipments
    zone_equipment_max = 0
    for zone_hvac_equipment_list in all_zone_hvac_equipment_lists:
        num_elements = len(zone_hvac_equipment_list.equipment())
        if num_elements > zone_equipment_max:
            zone_equipment_max = num_elements
    
    for i in range(zone_equipment_max):
      all_zone_hvac_equipment_lists_df[f'Zone Equipment {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Cooling Sequence {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Heating or No-Load Sequence {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Sequential Cooling Fraction Schedule Name {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Sequential Heating Fraction Schedule Name {i+1}'] = None


    for index, row in all_zone_hvac_equipment_lists_df.iterrows():
      # Add columns for each zone HVAC equipment
      zone_hvac_equipment_list = osm_model.getZoneHVACEquipmentListByName(row['Name']).get()
      for i in range(len(zone_hvac_equipment_list.equipment())):
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment {i+1}'] = zone_hvac_equipment_list.equipment()[i].name().get()
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Cooling Sequence {i+1}'] = zone_hvac_equipment_list.coolingPriority(zone_hvac_equipment_list.equipment()[i])
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Heating or No-Load Sequence {i+1}'] = zone_hvac_equipment_list.heatingPriority(zone_hvac_equipment_list.equipment()[i])
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Sequential Cooling Fraction Schedule Name {i+1}'] = zone_hvac_equipment_list.sequentialCoolingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).get().name().get() if not zone_hvac_equipment_list.sequentialCoolingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).isNull() else None
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Sequential Heating Fraction Schedule Name {i+1}'] = zone_hvac_equipment_list.sequentialHeatingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).get().name().get() if not zone_hvac_equipment_list.sequentialHeatingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).isNull() else None

    print(
        f"The OSM model contains {all_zone_hvac_equipment_lists_df.shape[0]} thermal zones")

    return all_zone_hvac_equipment_lists_df



def get_all_zone_hvac_terminal_unit_variant_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all zone HVAC Variant Refrigerant Flow from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_zone_hvac_vrfs = osm_model.getZoneHVACTerminalUnitVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_zone_hvac_vrfs],
        'Name': [x.name().get() for x in all_zone_hvac_vrfs],
        'Terminal Unit Availability schedule': [x.terminalUnitAvailabilityschedule().name() for x in all_zone_hvac_vrfs],
        'Terminal Unit Air Inlet Node': None,
        'Terminal Unit Air Outlet Node': None,
        'Supply Air Flow Rate During Cooling Operation {m3/s}': [x.supplyAirFlowRateDuringCoolingOperation().get() if not x.supplyAirFlowRateDuringCoolingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Cooling is Needed {m3/s}': [x.supplyAirFlowRateWhenNoCoolingisNeeded().get() if not x.supplyAirFlowRateWhenNoCoolingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate During Heating Operation {m3/s}': [x.supplyAirFlowRateDuringHeatingOperation().get() if not x.supplyAirFlowRateDuringHeatingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Heating is Needed {m3/s}': [x.supplyAirFlowRateWhenNoHeatingisNeeded().get() if not x.supplyAirFlowRateWhenNoHeatingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Cooling Operation {m3/s}': [x.outdoorAirFlowRateDuringCoolingOperation().get() if not x.outdoorAirFlowRateDuringCoolingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Heating Operation {m3/s}': [x.outdoorAirFlowRateDuringHeatingOperation().get() if not x.outdoorAirFlowRateDuringHeatingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate When No Cooling or Heating is Needed {m3/s}': [x.outdoorAirFlowRateWhenNoCoolingorHeatingisNeeded().get() if not x.outdoorAirFlowRateWhenNoCoolingorHeatingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Fan Operating Mode Schedule': [x.supplyAirFanOperatingModeSchedule().name() if not x.supplyAirFanOperatingModeSchedule().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Fan Placement': [x.supplyAirFanPlacement() for x in all_zone_hvac_vrfs],
        'Supply Air Fan': [x.supplyAirFan().name().get() if not x.supplyAirFan().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Outside Air Mixer': None,
        'Cooling Coil': [x.coolingCoil().get().name().get() if not x.coolingCoil().get().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Heating Coil': [x.heatingCoil().get().name().get() if not x.heatingCoil().get().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Zone Terminal Unit On Parasitic Electric Energy Use {W}': [x.zoneTerminalUnitOnParasiticElectricEnergyUse() for x in all_zone_hvac_vrfs],
        'Zone Terminal Unit Off Parasitic Electric Energy Use {W}': [x.zoneTerminalUnitOffParasiticElectricEnergyUse() for x in all_zone_hvac_vrfs],
        'Rated Total Heating Capacity Sizing Ratio {W/W}': [x.ratedTotalHeatingCapacitySizingRatio() for x in all_zone_hvac_vrfs],
        'Availability Manager List Name': None,
        'Design Specification ZoneHVAC Sizing Object Name': None,
        'Supplemental Heating Coil Name': [x.supplementalHeatingCoil().get().name() if not x.supplementalHeatingCoil().isNull() else None for x in all_zone_hvac_vrfs],
        'Maximum Supply Air Temperature from Supplemental Heater {C}': [x.maximumSupplyAirTemperaturefromSupplementalHeater() for x in all_zone_hvac_vrfs],
        'Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation {C}': [x.maximumOutdoorDryBulbTemperatureforSupplementalHeaterOperation() for x in all_zone_hvac_vrfs]
        }
                       
    # Create a DataFrame of all thermal zones.
    all_zone_hvac_vrfs_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_zone_hvac_vrfs_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_zone_hvac_vrfs_df = all_zone_hvac_vrfs_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_zone_hvac_vrfs_df.shape[0]} thermal zones")

    return all_zone_hvac_vrfs_df


def get_air_terminal_single_duct_parallel_piu_reheat_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirTerminalSingleDuctParallelPIUReheat(
            handle)
        if osm_object is None:
            print(
                f"No air terminal single duct parallel PIU reheat object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirTerminalSingleDuctParallelPIUReheatByName(
            name)
        if not osm_object:
            print(
                f"No air terminal single duct parallel PIU reheat object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
                  'Handle': str(target_object.handle()),
                  'Name': target_object.name().get() if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
                  'Maximum Primary Air Flow Rate {m3/s}': target_object.maximumPrimaryAirFlowRate().get() if not target_object.isMaximumPrimaryAirFlowRateAutosized() else 'Autosize',
                  'Maximum Secondary Air Flow Rate {m3/s}': target_object.maximumSecondaryAirFlowRate().get() if not target_object.isMaximumPrimaryAirFlowRateAutosized() else 'Autosize',
                  'Minimum Primary Air Flow Fraction': target_object.minimumPrimaryAirFlowFraction().get() if not target_object.isMinimumPrimaryAirFlowFractionAutosized() else 'Autosize',                  
                  'Fan On Flow Fraction': target_object.fanOnFlowFraction().get() if not target_object.isFanOnFlowFractionAutosized() else 'Autosize',
                  'Supply Air Inlet Node Name': target_object.inletModelObject().get().nameString() if target_object.inletModelObject().is_initialized() else None,
                  'Secondary Air Inlet Node Name': target_object.secondaryAirInletNode().get().nameString() if target_object.secondaryAirInletNode().is_initialized() else None,                  
                  'Outlet Node Name': target_object.outletModelObject().get().nameString() if target_object.outletModelObject().is_initialized() else None,                
                  'Reheat Coil Air Inlet Node Name': None,
                  'Zone Mixer Name': None,
                  'Fan Name': target_object.fan().nameString(),
                  'Reheat Coil Name': target_object.reheatCoil().nameString(),
                  'Maximum Hot Water or Steam Flow Rate {m3/s}': target_object.maximumHotWaterorSteamFlowRate() if not target_object.isMaximumHotWaterorSteamFlowRateAutosized() else 'Autosize',
                  'Minimum Hot Water or Steam Flow Rate {m3/s}': target_object.minimumHotWaterorSteamFlowRate(),
                  'Convergence Tolerance': target_object.convergenceTolerance()
    }

    return object_dict

def get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dict(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all air terminal single duct parallel PIU reheat objects from the OpenStudio model 
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an air terminal single duct parallel PIU reheat object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getAirTerminalSingleDuctParallelPIUReheats()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_air_terminal_single_duct_parallel_piu_reheat_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all air terminal single duct parallel PIU reheat objects from the OpenStudio model 
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all air terminal single duct parallel PIU reheat objects.
    """

    all_objects_dicts = get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dict(osm_model)

    # Create a DataFrame of all air terminal single duct parallel PIU reheat objects.
    all_air_terminals_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_air_terminals_df = all_air_terminals_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_air_terminals_df.shape[0]} air terminal single duct parallel PIU reheat objects")

    return all_air_terminals_df

#------------------------
#--- ZoneHVAC:UnitHeater
#------------------------

def get_zone_hvac_unit_heater_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets ZoneHVAC:UnitHeater information and returns it as a dictionary.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model object.
        handle (str, optional): The handle of the ZoneHVAC:UnitHeater object. Either handle or name must be provided.
        name (str, optional): The name of the HVAC unit. Either name or handle must be provided.

    Returns:
        dict: A dictionary containing the ZoneHVAC:UnitHeater objects's properties, or an empty dictionary if not found.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getZoneHVACUnitHeater(handle)
        if osm_object is None:
            print(
                f"No Zone HVAC Unit Heater object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getZoneHVACUnitHeaterByName(name)
        if not osm_object:
            print(
                f"No Zone HVAC Unit Heater object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
                  'Handle': str(target_object.handle()),
                  'Name': target_object.name().get() if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
                  'Air Inlet Node Name': target_object.inletNode().get().nameString() if target_object.inletNode().is_initialized() else None,
                  'Air Outlet Node Name': target_object.outletNode().get().nameString() if target_object.outletNode().is_initialized() else None,
                  'Supply Air Fan Name': target_object.supplyAirFan().nameString(),
                  'Maximum Supply Air Flow Rate {m3/s}': target_object.maximumSupplyAirFlowRate() if not target_object.isMaximumSupplyAirFlowRateAutosized() else 'Autosize',                  
                  'Fan Control Type': target_object.fanControlType(),
                  'Heating Coil Name': target_object.heatingCoil().nameString(),
                  'Maximum Hot Water Flow Rate {m3/s}': target_object.maximumHotWaterFlowRate() if not target_object.isMaximumHotWaterFlowRateAutosized() else 'Autosize',
                  'Minimum Hot Water Flow Rate {m3/s}': target_object.minimumHotWaterFlowRate(),
                  'Heating Convergence Tolerance': target_object.heatingConvergenceTolerance(),
                  'Availability Manager List Name': None
    }

    return object_dict

def get_all_zone_hvac_unit_heater_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all ZoneHVAC:UnitHeater objects from the OpenStudio model 
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a ZoneHVAC:UnitHeater objects.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getZoneHVACUnitHeaters()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_zone_hvac_unit_heater_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_zone_hvac_unit_heater_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all ZoneHVAC:UnitHeater object from the OpenStudio model 
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all ZoneHVAC:UnitHeater objects.
    """

    all_objects_dicts = get_all_zone_hvac_unit_heater_objects_as_dicts(osm_model)

    # Create a DataFrame of all ZoneHVAC:UnitHeater objects.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} ZoneHVAC:UnitHeater objects")

    return all_objects_df

#-------------------------------
#--- OS:ZoneHVAC:FourPipeFanCoil
#-------------------------------

def get_four_pipe_fan_coil_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets ZoneHVAC:FourPipeFanCoil information and returns it as a dictionary.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model object.
        handle (str, optional): The handle of the ZoneHVAC:FourPipeFanCoil object. Either handle or name must be provided.
        name (str, optional): The name of the HVAC unit. Either name or handle must be provided.

    Returns:
        dict: A dictionary containing the ZoneHVAC:FourPipeFanCoil objects's properties, or an empty dictionary if not found.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getZoneHVACFourPipeFanCoil(handle)
        if osm_object is None:
            print(
                f"No ZoneHVAC:FourPipeFanCoil object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getZoneHVACFourPipeFanCoilByName(name)
        if not osm_object:
            print(
                f"No ZoneHVAC:FourPipeFanCoil object found with the name: {name}")
            return {}

    target_object = osm_object.get()
    object_dict = {
        'Handle': str(target_object.handle()),
                  'Name': target_object.name().get() if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
                  'Capacity Control Method': target_object.capacityControlMethod(),
                  'Maximum Supply Air Flow Rate {m3/s}': target_object.maximumSupplyAirFlowRate().get() if not target_object.isMaximumSupplyAirFlowRateAutosized() else 'autosize',                  
                  'Low Speed Supply Air Flow Ratio': target_object.lowSpeedSupplyAirFlowRatio(),
                  'Medium Speed Supply Air Flow Ratio': target_object.mediumSpeedSupplyAirFlowRatio(),                  
                  'Maximum Outdoor Air Flow Rate {m3/s}': target_object.maximumOutdoorAirFlowRate().get() if not target_object.isMaximumOutdoorAirFlowRateAutosized() else 'autosize',
                  'Outdoor Air Schedule Name': target_object.outdoorAirSchedule().get().name().get() if target_object.outdoorAirSchedule().is_initialized() else None,
                  'Air Inlet Node Name': target_object.inletNode().get().nameString() if target_object.inletNode().is_initialized() else None,
                  'Air Outlet Node Name':target_object.outletNode().get().nameString() if target_object.outletNode().is_initialized() else None,
                  'Outdoor Air Mixer Object Type': target_object.outdoorAirMixerObjectType(),
                  'Outdoor Air Mixer Name': target_object.outdoorAirMixerName(),
                  'Supply Air Fan Name': target_object.supplyAirFan().nameString(),
                  'Cooling Coil Name': target_object.coolingCoil().nameString(),
                  'Maximum Cold Water Flow Rate {m3/s}': target_object.maximumColdWaterFlowRate() if not target_object.isMaximumHotWaterFlowRateAutosized() else 'autosize',
                  'Minimum Cold Water Flow Rate {m3/s}': target_object.minimumColdWaterFlowRate(),
                  'Cooling Convergence Tolerance': target_object.coolingConvergenceTolerance(),
                  'Heating Coil Name': target_object.heatingCoil().nameString(),
                  'Maximum Hot Water Flow Rate {m3/s}': target_object.maximumHotWaterFlowRate() if not target_object.isMaximumHotWaterFlowRateAutosized() else 'autosize',
                  'Minimum Hot Water Flow Rate {m3/s}': target_object.minimumHotWaterFlowRate(),
                  'Heating Convergence Tolerance': target_object.heatingConvergenceTolerance(),
                  'Supply Air Fan Operating Mode Schedule Name': None,
                  'Minimum Supply Air Temperature in Cooling Mode {C}': target_object.minimumSupplyAirTemperatureInCoolingMode() if not target_object.isMinimumSupplyAirTemperatureInCoolingModeAutosized() else 'autosize',
                  'Maximum Supply Air Temperature in Heating Mode {C}': target_object.maximumSupplyAirTemperatureInHeatingMode() if not target_object.isMaximumSupplyAirTemperatureInHeatingModeAutosized() else 'autosize'
              }

    return object_dict

def get_all_four_pipe_fan_coil_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all ZoneHVAC:FourPipeFanCoil objects from the OpenStudio model
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a ZoneHVAC:FourPipeFanCoil objects.
    """

    # Get all ZoneHVAC:FourPipeFanCoil objects in the OpenStudio model.
    all_objects = osm_model.getZoneHVACFourPipeFanCoils()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_four_pipe_fan_coil_object_as_dict(osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_four_pipe_fan_coil_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all ZoneHVAC:FourPipeFanCoil objects from the OpenStudio model
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all ZoneHVAC:FourPipeFanCoil objects.
    """

    all_objects_dicts = get_all_four_pipe_fan_coil_objects_as_dicts(osm_model)

    # Create a DataFrame of all ZoneHVAC:FourPipeFanCoil objects.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} ZoneHVAC:FourPipeFanCoil objects")

    return all_objects_df
