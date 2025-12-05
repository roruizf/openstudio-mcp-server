import openstudio
import pandas as pd


def get_thermal_zone_object_as_dict(osm_model: openstudio.model.Model, zone_handle: str = None, zone_name: str = None) -> dict:
    """
    Retrieve a thermal zone from the OpenStudio model by either handle or name and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - zone_handle (str, optional): The handle of the thermal zone to retrieve.
    - zone_name (str, optional): The name of the thermal zone to retrieve.

    Returns:
    - dict: Dictionary containing information about the specified thermal zone.
    """

    if zone_handle is not None and zone_name is not None:
        raise ValueError(
            "Only one of 'zone_handle' or 'zone_name' should be provided.")
    if zone_handle is None and zone_name is None:
        raise ValueError(
            "Either 'zone_handle' or 'zone_name' must be provided.")

    # Find the thermal zone by handle or name
    if zone_handle is not None:
        zone_object = osm_model.getThermalZone(zone_handle)
        if zone_object.isNull():
            print(f"No thermal zone found with the handle: {zone_handle}")
            return {}

    elif zone_name is not None:
        zone_object = osm_model.getThermalZoneByName(zone_name)
        if zone_object.isNull():
            print(f"No thermal zone found with the name: {zone_name}")
            return {}

    target_zone = zone_object.get()

    # Define attributes to retrieve in a dictionary
    zone_dict = {
        'Handle': str(target_zone.handle()),
        'Name': target_zone.name().get() if target_zone.name().is_initialized() else None,
        'Multiplier': target_zone.multiplier(),
        'Ceiling Height {m}': target_zone.ceilingHeight().get() if target_zone.ceilingHeight().is_initialized() else None,
        'Volume {m3}': target_zone.airVolume(),
        'Floor Area {m2}': target_zone.floorArea(),        
        'Zone Inside Convection Algorithm': target_zone.zoneInsideConvectionAlgorithm().get() if target_zone.zoneInsideConvectionAlgorithm().is_initialized() else None,
        'Zone Outside Convection Algorithm': target_zone.zoneOutsideConvectionAlgorithm().get() if target_zone.zoneOutsideConvectionAlgorithm().is_initialized() else None,
        'Zone Conditioning Equipment List Name': target_zone.zoneConditioningEquipmentListName(),
        'Zone Air Inlet Port List': str(target_zone.inletPortList().handle()) if not target_zone.inletPortList().handle().isNull() else None,
        'Zone Air Exhaust Port List': str(target_zone.exhaustPortList().handle()) if not target_zone.exhaustPortList().handle().isNull() else None,
        'Zone Air Node Name': target_zone.zoneAirNode().name().get() if target_zone.zoneAirNode().name().is_initialized() else None,
        'Zone Return Air Port List': str(target_zone.returnPortList().handle()) if not target_zone.returnPortList().handle().isNull() else None,
        'Primary Daylighting Control Name': target_zone.primaryDaylightingControl().get().name().get() if (target_zone.primaryDaylightingControl().is_initialized() and target_zone.primaryDaylightingControl().get().name().is_initialized) else None,
        'Fraction of Zone Controlled by Primary Daylighting Control': target_zone.fractionofZoneControlledbyPrimaryDaylightingControl(),
        'Secondary Daylighting Control Name': target_zone.secondaryDaylightingControl().get().name().get() if (target_zone.secondaryDaylightingControl().is_initialized() and target_zone.secondaryDaylightingControl().get().name().is_initialized()) else None,
        'Fraction of Zone Controlled by Secondary Daylighting Control': target_zone.fractionofZoneControlledbySecondaryDaylightingControl(),
        'Illuminance Map Name': target_zone.illuminanceMap().get().name().get() if (target_zone.illuminanceMap().is_initialized() and target_zone.illuminanceMap().get().name().is_initialized) else None,
        'Group Rendering Name': target_zone.renderingColor().get().name().get() if (target_zone.renderingColor().is_initialized() and target_zone.renderingColor().get().name().is_initialized) else None,
        'Thermostat Name': target_zone.thermostat().get().name().get() if(target_zone.thermostat().is_initialized() and target_zone.thermostat().get().name().is_initialized()) else None,
        'Use Ideal Air Loads': target_zone.useIdealAirLoads(),
        'Humidistat Name': target_zone.zoneControlHumidistat().get().name().get() if target_zone.zoneControlHumidistat().is_initialized() else None,
        'Daylighting Controls Availability Schedule Name': target_zone.daylightingControlsAvailabilitySchedule().get().name().get() if target_zone.daylightingControlsAvailabilitySchedule().is_initialized() else None
    }

    return zone_dict

def get_all_thermal_zones_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all thermal zones from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a thermal zone.
    """

    # Get all thermal zones in the OpenStudio model.
    all_objects = osm_model.getThermalZones()

    all_objects_dicts = []

    for target_object in all_objects:
        thermal_zone_handle = str(target_object.handle())
        object_dict = get_thermal_zone_object_as_dict(osm_model, thermal_zone_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

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