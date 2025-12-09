import openstudio
import pandas as pd

#--
#-- OS:Sizing:Zone
#--

def get_all_sizing_zone_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all zone Sizing Zone Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_sizing_zones = osm_model.getSizingZones()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_sizing_zones],
        'Zone or ZoneList Name': [x.thermalZone().name().get() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Temperature Input Method': [x.zoneCoolingDesignSupplyAirTemperatureInputMethod() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Temperature {C}': [x.zoneCoolingDesignSupplyAirTemperature() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Temperature Difference {deltaC}': [x.zoneCoolingDesignSupplyAirTemperatureDifference() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Temperature Input Method': [x.zoneHeatingDesignSupplyAirTemperatureInputMethod() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Temperature {C}': [x.zoneHeatingDesignSupplyAirTemperature() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Temperature Difference {deltaC}': [x.zoneHeatingDesignSupplyAirTemperatureDifference() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-air}': [x.zoneCoolingDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Humidity Ratio {kg-H2O/kg-air}': [x.zoneHeatingDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Heating Sizing Factor': [x.zoneHeatingSizingFactor() for x in all_sizing_zones],
        'Zone Cooling Sizing Factor': [x.zoneCoolingSizingFactor() for x in all_sizing_zones],
        'Cooling Design Air Flow Method': [x.coolingDesignAirFlowMethod() for x in all_sizing_zones],
        'Cooling Design Air Flow Rate {m3/s}': [x.coolingDesignAirFlowRate() for x in all_sizing_zones],
        'Cooling Minimum Air Flow per Zone Floor Area {m3/s-m2}': [x.coolingMinimumAirFlowperZoneFloorArea() for x in all_sizing_zones],
        'Cooling Minimum Air Flow {m3/s}': [x.coolingMinimumAirFlow() for x in all_sizing_zones],
        'Cooling Minimum Air Flow Fraction': [x.coolingMinimumAirFlowFraction() for x in all_sizing_zones],
        'Heating Design Air Flow Method': [x.heatingDesignAirFlowMethod() for x in all_sizing_zones],
        'Heating Design Air Flow Rate {m3/s}': [x.heatingDesignAirFlowRate() for x in all_sizing_zones],
        'Heating Maximum Air Flow per Zone Floor Area {m3/s-m2}': [x.heatingMaximumAirFlowperZoneFloorArea() for x in all_sizing_zones],
        'Heating Maximum Air Flow {m3/s}': [x.heatingMaximumAirFlow() for x in all_sizing_zones],
        'Heating Maximum Air Flow Fraction': [x.heatingMaximumAirFlowFraction() for x in all_sizing_zones],
        'Account for Dedicated Outdoor Air System': [x.accountforDedicatedOutdoorAirSystem() for x in all_sizing_zones],
        'Dedicated Outdoor Air System Control Strategy': [x.dedicatedOutdoorAirSystemControlStrategy() for x in all_sizing_zones],
        'Dedicated Outdoor Air Low Setpoint Temperature for Design {C}': [x.dedicatedOutdoorAirLowSetpointTemperatureforDesign() for x in all_sizing_zones],
        'Dedicated Outdoor Air High Setpoint Temperature for Design {C}': [x.dedicatedOutdoorAirHighSetpointTemperatureforDesign() for x in all_sizing_zones],
        'Zone Load Sizing Method': [x.zoneLoadSizingMethod() for x in all_sizing_zones],
        'Zone Latent Cooling Design Supply Air Humidity Ratio Input Method': [x.zoneLatentCoolingDesignSupplyAirHumidityRatioInputMethod() for x in all_sizing_zones],
        'Zone Dehumidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': [x.zoneDehumidificationDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': [x.zoneCoolingDesignSupplyAirHumidityRatioDifference() for x in all_sizing_zones],
        'Zone Latent Heating Design Supply Air Humidity Ratio Input Method': [x.zoneLatentHeatingDesignSupplyAirHumidityRatioInputMethod() for x in all_sizing_zones],
        'Zone Humidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': [x.zoneHumidificationDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Humidification Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': [x.zoneHumidificationDesignSupplyAirHumidityRatioDifference() for x in all_sizing_zones]
        }
    # Create a DataFrame of all thermal zones.
    all_sizing_zones_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_sizing_zones_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_sizing_zones_df = all_sizing_zones_df.sort_values(
        by='Zone or ZoneList Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_sizing_zones_df.shape[0]} sizing zones")

    return all_sizing_zones_df


#---
#--- OS:Sizing:System
#---

def get_sizing_system_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieves Sizing:System object information and returns it as a dictionary.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model containing the Sizing:System object.
        handle (str, optional): The handle of the Sizing:System object. Either handle or name must be provided.
        name (str, optional): The name of the Sizing:System object. Either name or handle must be provided.

    Returns:
        dict: A dictionary containing the Sizing:System object's properties, or an empty dictionary if not found.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getSizingSystem(handle)
        if osm_object is None:
            print(
                f"No Sizing:System object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getSizingSystemByName(name)
        if not osm_object:
            print(
                f"No Sizing:System object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
    'Handle': str(target_object.handle()),
    'AirLoop Name': target_object.airLoopHVAC().name().get() if target_object.airLoopHVAC().name().is_initialized() else None,    
    'Type of Load to Size On': target_object.typeofLoadtoSizeOn(),
    'Design Outdoor Air Flow Rate {m3/s}': target_object.designOutdoorAirFlowRate().get() if not target_object.isDesignOutdoorAirFlowRateAutosized() else 'Autosize',    
    'Central Heating Maximum System Air Flow Ratio': target_object.centralHeatingMaximumSystemAirFlowRatio().get() if not target_object.isCentralHeatingMaximumSystemAirFlowRatioAutosized() else 'Autosize',
    'Preheat Design Temperature {C}': target_object.preheatDesignTemperature(),
    'Preheat Design Humidity Ratio {kg-H2O/kg-Air}': target_object.preheatDesignHumidityRatio(),
    'Precool Design Temperature {C}': target_object.precoolDesignTemperature(),
    'Precool Design Humidity Ratio {kg-H2O/kg-Air}': target_object.precoolDesignHumidityRatio(),
    'Central Cooling Design Supply Air Temperature {C}': target_object.centralCoolingDesignSupplyAirTemperature(),
    'Central Heating Design Supply Air Temperature {C}': target_object.centralHeatingDesignSupplyAirTemperature(),
    'Sizing Option': target_object.sizingOption(),
    '100% Outdoor Air in Cooling': target_object.allOutdoorAirinCooling(),
    '100% Outdoor Air in Heating': target_object.allOutdoorAirinHeating(),    
    'Central Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-Air}': target_object.centralCoolingDesignSupplyAirHumidityRatio(),
    'Central Heating Design Supply Air Humidity Ratio {kg-H2O/kg-Air}': target_object.centralHeatingDesignSupplyAirHumidityRatio(),
    'Cooling Design Air Flow Method': target_object.coolingDesignAirFlowMethod(),
    'Cooling Design Air Flow Rate {m3/s}': target_object.coolingDesignAirFlowRate(),
    'Heating Design Air Flow Method': target_object.heatingDesignAirFlowMethod(),
    'Heating Design Air Flow Rate {m3/s}': target_object.heatingDesignAirFlowRate(),
    'System Outdoor Air Method': target_object.systemOutdoorAirMethod(),
    'Zone Maximum Outdoor Air Fraction {dimensionless}': target_object.zoneMaximumOutdoorAirFraction(),
    'Cooling Supply Air Flow Rate Per Floor Area {m3/s-m2}': target_object.coolingSupplyAirFlowRatePerFloorArea(),
    'Cooling Fraction of Autosized Cooling Supply Air Flow Rate': target_object.coolingFractionofAutosizedCoolingSupplyAirFlowRate(),
    'Cooling Supply Air Flow Rate Per Unit Cooling Capacity {m3/s-W}': target_object.coolingSupplyAirFlowRatePerUnitCoolingCapacity(),
    'Heating Supply Air Flow Rate Per Floor Area {m3/s-m2}': target_object.heatingSupplyAirFlowRatePerFloorArea(),
    'Heating Fraction of Autosized Heating Supply Air Flow Rate': target_object.heatingFractionofAutosizedCoolingSupplyAirFlowRate(),
    'Heating Fraction of Autosized Cooling Supply Air Flow Rate': target_object.heatingFractionofAutosizedCoolingSupplyAirFlowRate(),
    'Heating Supply Air Flow Rate Per Unit Heating Capacity {m3/s-W}': target_object.heatingSupplyAirFlowRatePerUnitHeatingCapacity(),
    'Cooling Design Capacity Method': target_object.coolingDesignCapacityMethod(),
    'Cooling Design Capacity {W}': target_object.coolingDesignCapacity().get() if not target_object.isCoolingDesignCapacityAutosized() else 'autosize',
    'Cooling Design Capacity Per Floor Area {W/m2}': target_object.coolingDesignCapacityPerFloorArea(),
    'Fraction of Autosized Cooling Design Capacity': target_object.fractionofAutosizedCoolingDesignCapacity(),
    'Heating Design Capacity Method': target_object.heatingDesignCapacityMethod(), 
    'Heating Design Capacity {W}': target_object.heatingDesignCapacity() if not target_object.isHeatingDesignCapacityAutosized() else 'autosize',
    'Heating Design Capacity Per Floor Area {W/m2}': target_object.heatingDesignCapacityPerFloorArea(),
    'Fraction of Autosized Heating Design Capacity': target_object.fractionofAutosizedHeatingDesignCapacity(),
    'Central Cooling Capacity Control Method': target_object.centralCoolingCapacityControlMethod(),
    'Occupant Diversity': target_object.occupantDiversity() if not target_object.isOccupantDiversityAutosized() else 'autosize',
}
    return object_dict


def get_all_air_sizing_system_objects_as_dict(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all Sizing:System objects from the OpenStudio model
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a Sizing:System object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getSizingSystems()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_sizing_system_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_air_sizing_system_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Sizing:System objects from the OpenStudio model
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all Sizing:System objects.
    """

    all_objects_dicts = get_all_air_sizing_system_objects_as_dict(osm_model)

    # Create a DataFrame of all Sizing:System objects.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='AirLoop Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} Sizing:System objects")

    return all_objects_df
