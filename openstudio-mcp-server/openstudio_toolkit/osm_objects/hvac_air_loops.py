import openstudio
import pandas as pd

#-------------------
#--- OS:AirLoopHVAC
#-------------------
def get_air_loop_hvac_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieves Air Loop HVAC information and returns it as a dictionary.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model containing the Air Loop HVAC unit.
        handle (str, optional): The handle of the HVAC unit. Either handle or name must be provided.
        name (str, optional): The name of the Air Loop HVAC object. Either name or handle must be provided.

    Returns:
        dict: A dictionary containing the Air Loop HVAC's properties, or an empty dictionary if not found.
    """
        
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirLoopHVAC(
            handle)
        if osm_object is None:
            print(
                f"No Air Loop HVAC  object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirLoopHVACByName(
            name)
        if not osm_object:
            print(
                f"No Air Loop HVAC  object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Controller List Name': None,
        'Availability Schedule': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Availability Manager List Name': None,
        'Design Supply Air Flow Rate {m3/s}': target_object.designSupplyAirFlowRate().get() if not target_object.isDesignSupplyAirFlowRateAutosized() else 'Autosize',
        'Design Return Air Flow Fraction of Supply Air Flow': target_object.designReturnAirFlowFractionofSupplyAirFlow(),
        'Branch List Name': None,
        'Connector List Name': None,
        'Supply Side Inlet Node Name': target_object.supplyInletNode().nameString(),
        'Demand Side Outlet Node Name': target_object.demandOutletNode().nameString(),
        'Demand Side Inlet Node A': target_object.demandInletNode().nameString(),
        'Supply Side Outlet Node A': target_object.supplyOutletNode().nameString(),
        'Demand Side Inlet Node B': None,
        'Supply Side Outlet Node B': None,
        'Return Air Bypass Flow Temperature Setpoint Schedule Name': None,
        'Demand Mixer Name': target_object.demandMixer().nameString(),
        'Demand Splitter A Name': target_object.demandSplitter().nameString(),
        'Demand Splitter B Name': None,
        'Supply Splitter Name': None}
    return object_dict


def get_all_air_loop_hvac_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all Air Loop HVAC objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about Air Loop HVAC objects.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getAirLoopHVACs()

    all_objects_dicts = []

    for target_object in all_objects:
        air_loop_hvac_handle = str(target_object.handle())
        object_dict = get_air_loop_hvac_object_as_dict(
            osm_model, air_loop_hvac_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_air_loop_hvac_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Air Loop HVAC objects from the OpenStudio model using a specified method and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all Air Loop HVAC objects.
    """

    all_objects_dicts = get_all_air_loop_hvac_objects_as_dicts(osm_model)

    # Create a DataFrame of all spaces.
    all_air_loop_hvac_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_air_loop_hvac_df = all_air_loop_hvac_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_air_loop_hvac_df.shape[0]} Air Loop HVAC objects")

    return all_air_loop_hvac_df

#------------------------------------
#--- OS:AirLoopHVAC:OutdoorAirSystem
#------------------------------------

def get_air_loop_hvac_outdoor_air_system_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets AirLoopHVAC:OutdoorAirSystem information and returns it as a dictionary.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model object.
        handle (str, optional): The handle of the AirLoopHVAC:OutdoorAirSystem object. Either handle or name must be provided.
        name (str, optional): The name of the HVAC unit. Either name or handle must be provided.

    Returns:
        dict: A dictionary containing the AirLoopHVAC:OutdoorAirSystem objects's properties, or an empty dictionary if not found.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirLoopHVACOutdoorAirSystem(handle)
        if osm_object is None:
            print(
                f"No AirLoopHVAC:OutdoorAirSystem object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirLoopHVACOutdoorAirSystemByName(name)
        if not osm_object:
            print(
                f"No AirLoopHVAC:OutdoorAirSystem object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Controller Name': target_object.getControllerOutdoorAir().name().get() if target_object.getControllerOutdoorAir().name().is_initialized() else None,
        'Outdoor Air Equipment List Name': None,
        'Availability Manager List Name': None,
        'Mixed Air Node Name': None,
        'Outdoor Air Stream Node Name': None,
        'Relief Air Stream Node Name': None,
        'Return Air Stream Node Name': None
        }

    return object_dict

def get_all_air_loop_hvac_outdoor_air_system_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all AirLoopHVAC:OutdoorAirSystem objects from the OpenStudio model
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a AirLoopHVAC:OutdoorAirSystem objects.
    """

    # Get all AirLoopHVAC:OutdoorAirSystem objects in the OpenStudio model.
    all_objects = osm_model.getAirLoopHVACOutdoorAirSystems()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_air_loop_hvac_outdoor_air_system_object_as_dict(osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_air_loop_hvac_outdoor_air_system_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all AirLoopHVAC:OutdoorAirSystem objects from the OpenStudio model
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all AirLoopHVAC:OutdoorAirSystem objects.
    """

    all_objects_dicts = get_all_air_loop_hvac_outdoor_air_system_objects_as_dicts(osm_model)

    # Create a DataFrame of all AirLoopHVAC:OutdoorAirSystem objects.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} AirLoopHVAC:OutdoorAirSystem objects")

    return all_objects_df

#---------------------------------
#--- OS:AirLoopHVAC:UnitarySystem
#---------------------------------

def get_air_loop_hvac_unitary_system_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieves AirLoopHVAC:UnitarySystem object information and returns it as a dictionary.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model containing the AirLoopHVAC:UnitarySystem object.
        handle (str, optional): The handle of the AirLoopHVAC:UnitarySystem object. Either handle or name must be provided.
        name (str, optional): The name of the AirLoopHVAC:UnitarySystem object. Either name or handle must be provided.

    Returns:
        dict: A dictionary containing the AirLoopHVAC:UnitarySystem object's properties, or an empty dictionary if not found.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirLoopHVACUnitarySystem(handle)
        if osm_object is None:
            print(
                f"No AirLoopHVAC:UnitarySystem object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirLoopHVACUnitarySystemByName(name)
        if not osm_object:
            print(
                f"No AirLoopHVAC:UnitarySystem object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
    'Handle': str(target_object.handle()),
    'Name': target_object.name().get() if target_object.name().is_initialized() else None,
    "Control Type": target_object.controlType(),
    "Controlling Zone or Thermostat Location": target_object.controllingZoneorThermostatLocation().get().nameString(),
    "Dehumidification Control Type": target_object.dehumidificationControlType(),
    'Availability Schedule Name': target_object.availabilitySchedule().get().name().get() if target_object.availabilitySchedule().get().name().is_initialized() else None,
    "Air Inlet Node Name": target_object.inletNode().get().name().get() if target_object.inletNode().get().name().is_initialized() else None,
    "Air Outlet Node Name": target_object.outletNode().get().name().get() if target_object.outletNode().get().name().is_initialized() else None,
    "Supply Fan Name": target_object.supplyFan().get().name().get() if target_object.supplyFan().get().name().is_initialized() else None,
    "Fan Placement": target_object.fanPlacement().get(),
    "Supply Air Fan Operating Mode Schedule Name": target_object.supplyAirFanOperatingModeSchedule().get().name().get() if target_object.supplyAirFanOperatingModeSchedule().get().name().is_initialized() else None,
    "Heating Coil Name": target_object.heatingCoil().get().name().get() if target_object.heatingCoil().get().name().is_initialized() else None,
    "DX Heating Coil Sizing Ratio": target_object.dXHeatingCoilSizingRatio(),
    "Cooling Coil Name": target_object.coolingCoil().get().name().get() if target_object.coolingCoil().get().name().is_initialized() else None,
    "Use DOAS DX Cooling Coil": target_object.useDOASDXCoolingCoil(),
    "DOAS DX Cooling Coil Leaving Minimum Air Temperature {C}": target_object.useDOASDXCoolingCoil(),
    "Latent Load Control": target_object.latentLoadControl(),
    "Supplemental Heating Coil Name": target_object.supplementalHeatingCoil().get().name().get() if target_object.supplementalHeatingCoil().get().name().is_initialized() else None,
    "Supply Air Flow Rate Method During Cooling Operation": target_object.supplyAirFlowRateMethodDuringCoolingOperation(),
    "Supply Air Flow Rate During Cooling Operation {m3/s}": target_object.supplyAirFlowRateDuringCoolingOperation().get() if not target_object.isSupplyAirFlowRateDuringCoolingOperationAutosized() else 'Autosize',    
    "Supply Air Flow Rate Per Floor Area During Cooling Operation {m3/s-m2}": target_object.supplyAirFlowRatePerFloorAreaDuringCoolingOperation().get() if target_object.supplyAirFlowRatePerFloorAreaDuringCoolingOperation().is_initialized() else None,    
    "Fraction of Autosized Design Cooling Supply Air Flow Rate": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Cooling Operation {m3/s-W}": None,
    "Supply Air Flow Rate Method During Heating Operation": target_object.supplyAirFlowRateMethodDuringHeatingOperation(),
    "Supply Air Flow Rate During Heating Operation {m3/s}": target_object.supplyAirFlowRateDuringHeatingOperation().get() if not target_object.isSupplyAirFlowRateDuringHeatingOperationAutosized() else 'Autosize',
    "Supply Air Flow Rate Per Floor Area during Heating Operation {m3/s-m2}": None,
    "Fraction of Autosized Design Heating Supply Air Flow Rate": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Heating Operation {m3/s-W}": None,
    "Supply Air Flow Rate Method When No Cooling or Heating is Required": None,
    "Supply Air Flow Rate When No Cooling or Heating is Required {m3/s}": None,
    "Supply Air Flow Rate Per Floor Area When No Cooling or Heating is Required {m3/s-m2}": None,
    "Fraction of Autosized Design Cooling Supply Air Flow Rate When No Cooling or Heating is Required": None,
    "Fraction of Autosized Design Heating Supply Air Flow Rate When No Cooling or Heating is Required": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Cooling Operation When No Cooling or Heating is Required {m3/s-W}": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Heating Operation When No Cooling or Heating is Required {m3/s-W}": None,
    "Maximum Supply Air Temperature {C}": target_object.maximumSupplyAirTemperature().get(),
    "Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation {C}": target_object.maximumOutdoorDryBulbTemperatureforSupplementalHeaterOperation(),
    "Outdoor Dry-Bulb Temperature Sensor Node Name": None,
    "Ancilliary On-Cycle Electric Power {W}": target_object.ancilliaryOnCycleElectricPower(),
    "Ancilliary Off-Cycle Electric Power {W}": target_object.ancilliaryOffCycleElectricPower()
}


    return object_dict

def get_all_air_loop_hvac_unitary_system_objects_as_dict(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all AirLoopHVAC:UnitarySystem objects from the OpenStudio model
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a AirLoopHVAC:UnitarySystem object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getAirLoopHVACUnitarySystems()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_air_loop_hvac_unitary_system_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_air_loop_hvac_unitary_system_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all AirLoopHVAC:UnitarySystem objects from the OpenStudio model
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all AirLoopHVAC:UnitarySystem objects.
    """

    all_objects_dicts = get_all_air_loop_hvac_unitary_system_objects_as_dict(osm_model)

    # Create a DataFrame of all AirLoopHVAC:UnitarySystem objects.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} AirLoopHVAC:UnitarySystem objects")

    return all_objects_df