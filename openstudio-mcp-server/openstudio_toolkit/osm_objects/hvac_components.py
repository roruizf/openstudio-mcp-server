import openstudio
import pandas as pd

def get_all_coil_cooling_dx_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Coil Cooling DX Variable Refrigerant Flow Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_coil_cooling_dx_vrfs = osm_model.getCoilCoolingDXVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_coil_cooling_dx_vrfs],
        'Name': [x.name().get() for x in all_coil_cooling_dx_vrfs],
        'Availability Schedule': [x.availabilitySchedule().name().get() for x in all_coil_cooling_dx_vrfs],
        'Rated Total Cooling Capacity {W}': [x.ratedTotalCoolingCapacity().get() if not x.ratedTotalCoolingCapacity().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Rated Sensible Heat Ratio': [x.ratedSensibleHeatRatio().get() if not x.ratedSensibleHeatRatio().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Rated Air Flow Rate {m3/s}': [x.ratedAirFlowRate().get() if not x.ratedAirFlowRate().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Cooling Capacity Ratio Modifier Function of Temperature Curve': [x.coolingCapacityRatioModifierFunctionofTemperatureCurve().name().get() if not x.coolingCapacityRatioModifierFunctionofTemperatureCurve().name().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Cooling Capacity Modifier Curve Function of Flow Fraction': [x.coolingCapacityModifierCurveFunctionofFlowFraction().name().get() if not x.coolingCapacityModifierCurveFunctionofFlowFraction().name().isNull() else None for x in all_coil_cooling_dx_vrfs]
    }
    
    # Create a DataFrame of Coil Cooling DX Variable Refrigerant Flow Objects.
    all_coil_cooling_dx_vrfs_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_coil_cooling_dx_vrfs_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_coil_cooling_dx_vrfs_df = all_coil_cooling_dx_vrfs_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_coil_cooling_dx_vrfs_df.shape[0]} sizing zones")

    return all_coil_cooling_dx_vrfs_df


def get_all_coil_heating_dx_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Coil Heating DX Variable Refrigerant Flow Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_coil_heating_dx_vrfs = osm_model.getCoilHeatingDXVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_coil_heating_dx_vrfs],
        'Name': [x.name().get() for x in all_coil_heating_dx_vrfs],
        'Availability Schedule': [x.availabilitySchedule().name().get() for x in all_coil_heating_dx_vrfs],
        'Rated Total Heating Capacity {W}': [x.ratedTotalHeatingCapacity().get() if not x.ratedTotalHeatingCapacity().isNull() else None for x in all_coil_heating_dx_vrfs],
        'Rated Air Flow Rate {m3/s}': [x.ratedAirFlowRate().get() if not x.ratedAirFlowRate().isNull() else None for x in all_coil_heating_dx_vrfs],
        'Coil Air Inlet Node': None,
        'Coil Air Outlet Node': None,
        'Heating Capacity Ratio Modifier Function of Temperature Curve': [x.heatingCapacityRatioModifierFunctionofTemperatureCurve().name().get() if not x.heatingCapacityRatioModifierFunctionofTemperatureCurve().name().isNull() else None for x in all_coil_heating_dx_vrfs],
        'Heating Capacity Modifier Function of Flow Fraction Curve': [x.heatingCapacityModifierFunctionofFlowFractionCurve().name().get() if not x.heatingCapacityModifierFunctionofFlowFractionCurve().name().isNull() else None for x in all_coil_heating_dx_vrfs]
    }
    
    # Create a DataFrame of Coil Heating DX Variable Refrigerant Flow Objects.
    all_coil_heating_dx_vrfs_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_coil_heating_dx_vrfs_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_coil_heating_dx_vrfs_df = all_coil_heating_dx_vrfs_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_coil_heating_dx_vrfs_df.shape[0]} sizing zones")

    return all_coil_heating_dx_vrfs_df

#--------------------------
#--- OS:Fan:ConstantVolume
#--------------------------

def get_all_fan_constant_volume_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Fan Constant Volume Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_fan_constant_volume = osm_model.getFanConstantVolumes()
    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_fan_constant_volume],
        'Name': [x.name().get() for x in all_fan_constant_volume],
        'Availability Schedule Name': [x.availabilitySchedule().name().get() if not x.availabilitySchedule().name().isNull() else None for x in all_fan_constant_volume],
        'Fan Total Efficiency': [x.fanTotalEfficiency() for x in all_fan_constant_volume],
        'Pressure Rise {Pa}': [x.pressureRise() for x in all_fan_constant_volume],
        'Maximum Flow Rate {m3/s}': [x.maximumFlowRate().get() if not x.maximumFlowRate().isNull() else None for x in all_fan_constant_volume],
        'Motor Efficiency': None,
        'Motor In Airstream Fraction': None,
        'Air Inlet Node Name': None,
        'Air Outlet Node Name': None,
        'End-Use Subcategory': [x.endUseSubcategory() for x in all_fan_constant_volume]
        }

    # Create a DataFrame of Fan Constant Volume Objects.
    all_fan_constant_volume_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_fan_constant_volume_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_fan_constant_volume_df = all_fan_constant_volume_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_fan_constant_volume_df.shape[0]} Fan Constant Volume Objects")

    return all_fan_constant_volume_df

#-----------------
#--- OS:Fan:OnOff
#-----------------

def get_all_fan_on_off_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Fan On Off Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_fan_on_off = osm_model.getFanOnOffs()
    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_fan_on_off],
        'Name': [x.name().get() for x in all_fan_on_off],
        'Availability Schedule Name': [x.availabilitySchedule().name().get() if not x.availabilitySchedule().name().isNull() else None for x in all_fan_on_off],
        'Fan Total Efficiency': [x.fanTotalEfficiency() for x in all_fan_on_off],
        'Pressure Rise {Pa}': [x.pressureRise() for x in all_fan_on_off],
        'Maximum Flow Rate {m3/s}': [x.maximumFlowRate().get() if not x.maximumFlowRate().isNull() else None for x in all_fan_on_off],
        'Motor Efficiency': [x.motorEfficiency() for x in all_fan_on_off],
        'Motor In Airstream Fraction': [x.motorInAirstreamFraction().get() if not x.motorInAirstreamFraction().isNull() else None for x in all_fan_on_off],
        'Air Inlet Node Name': [x.inletPort() for x in all_fan_on_off],
        'Air Outlet Node Name': [x.outletPort() for x in all_fan_on_off],
        'Fan Power Ratio Function of Speed Ratio Curve Name': [x.fanPowerRatioFunctionofSpeedRatioCurve().nameString() for x in all_fan_on_off],
        'Fan Efficiency Ratio Function of Speed Ratio Curve Name': [x.fanEfficiencyRatioFunctionofSpeedRatioCurve().nameString() for x in all_fan_on_off],
        'End-Use Subcategory': [x.endUseSubcategory() for x in all_fan_on_off]
        }

    # Create a DataFrame of Fan On Off Objects.
    all_fan_on_off_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_fan_on_off_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_fan_on_off_df = all_fan_on_off_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_fan_on_off_df.shape[0]} Fan On Off Objects")

    return all_fan_on_off_df

def get_all_hx_air_to_air_sensible_and_latent_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:  
  
  """
      Retrieve all Heat Exchanger Air To Air Sensible And Latent Objects from the OpenStudio model and organize them into a pandas DataFrame.

      Parameters:
      - osm_model (openstudio.model.Model): The OpenStudio Model object.

      Returns:
      - pd.DataFrame: DataFrame containing information about all Heat Exchanger Air To Air Sensible And Latent.
  """
  all_hx_air_to_air_sensible_and_latent = osm_model.getHeatExchangerAirToAirSensibleAndLatents()

  # Define attributes to retrieve in a dictionary
  object_attr = {
                'Handle': [str(x.handle()) for x in all_hx_air_to_air_sensible_and_latent],
                'Name': [x.name().get() for x in all_hx_air_to_air_sensible_and_latent],      
                'Availability Schedule': [x.availabilitySchedule().name().get() if not x.availabilitySchedule().name().isNull() else None for x in all_hx_air_to_air_sensible_and_latent],
                'Nominal Supply Air Flow Rate {m3/s}': [x.nominalSupplyAirFlowRate().get() if not x.nominalSupplyAirFlowRate().isNull() else None for x in all_hx_air_to_air_sensible_and_latent],
                'Sensible Effectiveness at 100% Heating Air Flow {dimensionless}': [x.sensibleEffectivenessat100HeatingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Latent Effectiveness at 100% Heating Air Flow {dimensionless}': [x.latentEffectivenessat100HeatingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Sensible Effectiveness at 100% Cooling Air Flow {dimensionless}': [x.sensibleEffectivenessat100CoolingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Latent Effectiveness at 100% Cooling Air Flow {dimensionless}': [x.latentEffectivenessat100CoolingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Supply Air Inlet Node': None,
                'Supply Air Outlet Node': None,
                'Exhaust Air Inlet Node': None,
                'Exhaust Air Outlet Node': None,
                'Nominal Electric Power {W}': [x.nominalElectricPower() for x in all_hx_air_to_air_sensible_and_latent],
                'Supply Air Outlet Temperature Control': [x.supplyAirOutletTemperatureControl() for x in all_hx_air_to_air_sensible_and_latent],
                'Heat Exchanger Type': [x.heatExchangerType() for x in all_hx_air_to_air_sensible_and_latent],
                'Frost Control Type': [x.frostControlType() for x in all_hx_air_to_air_sensible_and_latent],
                'Threshold Temperature {C}': [x.thresholdTemperature() for x in all_hx_air_to_air_sensible_and_latent],
                'Initial Defrost Time Fraction {dimensionless}': [x.initialDefrostTimeFraction() for x in all_hx_air_to_air_sensible_and_latent],
                'Rate of Defrost Time Fraction Increase {1/K}': [x.rateofDefrostTimeFractionIncrease() for x in all_hx_air_to_air_sensible_and_latent],
                'Economizer Lockout': [x.economizerLockout() for x in all_hx_air_to_air_sensible_and_latent],
                'Sensible Effectiveness of Heating Air Flow Curve Name': None,
                'Latent Effectiveness of Heating Air Flow Curve Name': None,
                'Sensible Effectiveness of Cooling Air Flow Curve Name': None,
                'Latent Effectiveness of Cooling Air Flow Curve Name': None
                }
  # Create a DataFrame of Heat Exchanger Air To Air Sensible And Latent Objects.
  all_hx_air_to_air_sensible_and_latent_df = pd.DataFrame(columns=object_attr.keys())
  for key in object_attr.keys():
      all_hx_air_to_air_sensible_and_latent_df[key] = object_attr[key]

  # Sort the DataFrame alphabetically by the Name column and reset indexes
  all_hx_air_to_air_sensible_and_latent_df = all_hx_air_to_air_sensible_and_latent_df.sort_values(
      by='Name', ascending=True).reset_index(drop=True)

  print(
      f"The OSM model contains {all_hx_air_to_air_sensible_and_latent_df.shape[0]} Heat Exchanger Air To Air Sensible And Latent Objects Objects")
  return all_hx_air_to_air_sensible_and_latent_df

def get_all_air_conditioner_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
        Retrieve all OS:AirConditioner:VariableRefrigerantFlow Objects from the OpenStudio model and organize them into a pandas DataFrame.

        Parameters:
        - osm_model (openstudio.model.Model): The OpenStudio Model object.

        Returns:
        - pd.DataFrame: DataFrame containing information about all OS:AirConditioner:VariableRefrigerantFlow objects.
    """
    all_objects = osm_model.getAirConditionerVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_objects],
        'Name': [x.name().get() for x in all_objects],
        'Availability Schedule': [x.availabilitySchedule().name() for x in all_objects],
        'Gross Rated Total Cooling Capacity {W}': [x.grossRatedTotalCoolingCapacity() for x in all_objects],
        'Gross Rated Cooling COP {W/W}': [x.grossRatedCoolingCOP() for x in all_objects],
        'Minimum Outdoor Temperature in Cooling Mode {C}': [x.minimumOutdoorTemperatureinCoolingMode() for x in all_objects],
        'Maximum Outdoor Temperature in Cooling Mode {C}': [x.maximumOutdoorTemperatureinCoolingMode() for x in all_objects],
        'Cooling Capacity Ratio Modifier Function of Low Temperature Curve Name': [x.coolingCapacityRatioModifierFunctionofLowTemperatureCurve().get().name() if not x.coolingCapacityRatioModifierFunctionofLowTemperatureCurve().isNull() else None for x in all_objects],
        'Cooling Capacity Ratio Boundary Curve Name': [x.coolingCapacityRatioBoundaryCurve().get().name() if not x.coolingCapacityRatioBoundaryCurve().isNull() else None for x in all_objects],
        'Cooling Capacity Ratio Modifier Function of High Temperature Curve Name': [x.coolingCapacityRatioModifierFunctionofHighTemperatureCurve().get().name() if not x.coolingCapacityRatioModifierFunctionofHighTemperatureCurve().isNull() else None for x in all_objects],
        'Cooling Energy Input Ratio Modifier Function of Low Temperature Curve Name': [x.coolingEnergyInputRatioModifierFunctionofLowTemperatureCurve().get().name() if not x.coolingEnergyInputRatioModifierFunctionofLowTemperatureCurve().isNull() else None for x in all_objects],
        'Cooling Energy Input Ratio Boundary Curve Name': [x.coolingEnergyInputRatioBoundaryCurve().get().name() if not x.coolingEnergyInputRatioBoundaryCurve().isNull() else None for x in all_objects],
        'Cooling Energy Input Ratio Modifier Function of High Temperature Curve Name': [x.coolingEnergyInputRatioModifierFunctionofHighTemperatureCurve().get().name() if not x.coolingEnergyInputRatioModifierFunctionofHighTemperatureCurve().isNull() else None for x in all_objects],
        'Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name': [x.coolingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().get().name() if not x.coolingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().isNull() else None for x in all_objects],
        'Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name': [x.coolingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().get().name() if not x.coolingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().isNull() else None for x in all_objects],
        'Cooling Combination Ratio Correction Factor Curve Name': [x.coolingCombinationRatioCorrectionFactorCurve().get().name() if not x.coolingCombinationRatioCorrectionFactorCurve().isNull() else None for x in all_objects],
        'Cooling Part-Load Fraction Correlation Curve Name': [x.coolingPartLoadFractionCorrelationCurve().get().name() if not x.coolingPartLoadFractionCorrelationCurve().isNull() else None for x in all_objects],
        'Gross Rated Heating Capacity {W}': [x.grossRatedHeatingCapacity() for x in all_objects],
        'Rated Heating Capacity Sizing Ratio {W/W}': [x.ratedHeatingCapacitySizingRatio() for x in all_objects],
        'Rated Heating COP {W/W}': [x.ratedHeatingCOP() for x in all_objects],
        'Minimum Outdoor Temperature in Heating Mode {C}': [x.minimumOutdoorTemperatureinHeatingMode() for x in all_objects],
        'Maximum Outdoor Temperature in Heating Mode {C}': [x.maximumOutdoorTemperatureinHeatingMode() for x in all_objects],
        'Heating Capacity Ratio Modifier Function of Low Temperature Curve Name': [x.heatingCapacityRatioModifierFunctionofLowTemperatureCurve().get().name() if not x.heatingCapacityRatioModifierFunctionofLowTemperatureCurve().isNull() else None for x in all_objects],
        'Heating Capacity Ratio Boundary Curve Name': [x.heatingCapacityRatioBoundaryCurve().get().name() if not x.heatingCapacityRatioBoundaryCurve().isNull() else None for x in all_objects],
        'Heating Capacity Ratio Modifier Function of High Temperature Curve Name': [x.heatingCapacityRatioModifierFunctionofHighTemperatureCurve().get().name() if not x.heatingCapacityRatioModifierFunctionofHighTemperatureCurve().isNull() else None for x in all_objects],
        'Heating Energy Input Ratio Modifier Function of Low Temperature Curve Name': [x.heatingEnergyInputRatioModifierFunctionofLowTemperatureCurve().get().name() if not x.heatingEnergyInputRatioModifierFunctionofLowTemperatureCurve().isNull() else None for x in all_objects],
        'Heating Energy Input Ratio Boundary Curve Name': [x.heatingEnergyInputRatioBoundaryCurve().get().name() if not x.heatingEnergyInputRatioBoundaryCurve().isNull() else None for x in all_objects],
        'Heating Energy Input Ratio Modifier Function of High Temperature Curve Name': [x.heatingEnergyInputRatioModifierFunctionofHighTemperatureCurve().get().name() if not x.heatingEnergyInputRatioModifierFunctionofHighTemperatureCurve().isNull() else None for x in all_objects],
        'Heating Performance Curve Outdoor Temperature Type': [x.heatingPerformanceCurveOutdoorTemperatureType() for x in all_objects],
        'Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name': [x.heatingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().get().name() if not x.heatingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().isNull() else None for x in all_objects],
        'Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name': [x.heatingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().get().name() if not x.heatingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().isNull() else None for x in all_objects],
        'Heating Combination Ratio Correction Factor Curve Name': [x.heatingCombinationRatioCorrectionFactorCurve().get().name() if not x.heatingCombinationRatioCorrectionFactorCurve().isNull() else None for x in all_objects],
        'Heating Part-Load Fraction Correlation Curve Name': [x.heatingPartLoadFractionCorrelationCurve().get().name() if not x.heatingPartLoadFractionCorrelationCurve().isNull() else None for x in all_objects],
        'Minimum Heat Pump Part-Load Ratio {dimensionless}': [x.minimumHeatPumpPartLoadRatio() for x in all_objects],
        'Zone Name for Master Thermostat Location': [x.zoneforMasterThermostatLocation().get().name() if not x.zoneforMasterThermostatLocation().isNull() else None for x in all_objects],
        'Master Thermostat Priority Control Type': [x.masterThermostatPriorityControlType() for x in all_objects],
        'Thermostat Priority Schedule': [x.thermostatPrioritySchedule().get().name() if not x.thermostatPrioritySchedule().isNull() else None for x in all_objects],
        'Zone Terminal Unit List': [None for x in all_objects],
        'Heat Pump Waste Heat Recovery': [x.heatPumpWasteHeatRecovery() for x in all_objects],
        'Equivalent Piping Length used for Piping Correction Factor in Cooling Mode {m}': [x.equivalentPipingLengthusedforPipingCorrectionFactorinCoolingMode() for x in all_objects],
        'Vertical Height used for Piping Correction Factor {m}': [x.verticalHeightusedforPipingCorrectionFactor() for x in all_objects],
        'Piping Correction Factor for Length in Cooling Mode Curve Name': [x.pipingCorrectionFactorforLengthinCoolingModeCurve().get().name() if not x.pipingCorrectionFactorforLengthinCoolingModeCurve().isNull() else None for x in all_objects],
        'Piping Correction Factor for Height in Cooling Mode Coefficient {1/m}': [x.pipingCorrectionFactorforHeightinCoolingModeCoefficient() for x in all_objects],
        'Equivalent Piping Length used for Piping Correction Factor in Heating Mode {m}': [x.equivalentPipingLengthusedforPipingCorrectionFactorinHeatingMode() for x in all_objects],
        'Piping Correction Factor for Length in Heating Mode Curve Name': [x.pipingCorrectionFactorforLengthinHeatingModeCurve().get().name() if not x.pipingCorrectionFactorforLengthinHeatingModeCurve().isNull() else None for x in all_objects],
        'Piping Correction Factor for Height in Heating Mode Coefficient {1/m}': [x.pipingCorrectionFactorforHeightinHeatingModeCoefficient() for x in all_objects],
        'Crankcase Heater Power per Compressor {W}': [x.crankcaseHeaterPowerperCompressor() for x in all_objects],
        'Number of Compressors {dimensionless}': [x.numberofCompressors() for x in all_objects],
        'Ratio of Compressor Size to Total Compressor Capacity {W/W}': [x.ratioofCompressorSizetoTotalCompressorCapacity() for x in all_objects],
        'Maximum Outdoor Dry-bulb Temperature for Crankcase Heater {C}': [x.maximumOutdoorDrybulbTemperatureforCrankcaseHeater() for x in all_objects],
        'Defrost Strategy': [x.defrostStrategy() for x in all_objects],
        'Defrost Control': [x.defrostControl() for x in all_objects],
        'Defrost Energy Input Ratio Modifier Function of Temperature Curve Name': [x.defrostEnergyInputRatioModifierFunctionofTemperatureCurve().get().name() if not x.defrostEnergyInputRatioModifierFunctionofTemperatureCurve().isNull() else None for x in all_objects],
        'Defrost Time Period Fraction {dimensionless}': [x.defrostTimePeriodFraction() for x in all_objects],
        'Resistive Defrost Heater Capacity {W}': [x.resistiveDefrostHeaterCapacity() for x in all_objects],
        'Maximum Outdoor Dry-bulb Temperature for Defrost Operation {C}': [x.maximumOutdoorDrybulbTemperatureforDefrostOperation() for x in all_objects],
        'Condenser Type': [x.condenserType() for x in all_objects],
        'Condenser Inlet Node': [None for x in all_objects],
        'Condenser Outlet Node': [None for x in all_objects],
        'Water Condenser Volume Flow Rate {m3/s}': [x.waterCondenserVolumeFlowRate() for x in all_objects],
        'Evaporative Condenser Effectiveness {dimensionless}': [x.evaporativeCondenserEffectiveness() for x in all_objects],
        'Evaporative Condenser Air Flow Rate {m3/s}': [x.evaporativeCondenserAirFlowRate() for x in all_objects],
        'Evaporative Condenser Pump Rated Power Consumption {W}': [x.evaporativeCondenserPumpRatedPowerConsumption() for x in all_objects],
        'Supply Water Storage Tank': [None for x in all_objects],
        'Basin Heater Capacity {W/K}': [x.basinHeaterCapacity() for x in all_objects],
        'Basin Heater Setpoint Temperature {C}': [x.basinHeaterSetpointTemperature() for x in all_objects],
        'Basin Heater Operating Schedule': [x.basinHeaterOperatingSchedule().get().name() if not x.basinHeaterOperatingSchedule().isNull() else None for x in all_objects],
        'Fuel Type': [x.fuelType() for x in all_objects],
        'Minimum Outdoor Temperature in Heat Recovery Mode {C}': [x.minimumOutdoorTemperatureinHeatRecoveryMode() for x in all_objects],
        'Maximum Outdoor Temperature in Heat Recovery Mode {C}': [x.maximumOutdoorTemperatureinHeatRecoveryMode() for x in all_objects],
        'Heat Recovery Cooling Capacity Modifier Curve Name': [x.heatRecoveryCoolingCapacityModifierCurve().get().name() if not x.heatRecoveryCoolingCapacityModifierCurve().isNull() else None for x in all_objects],
        'Initial Heat Recovery Cooling Capacity Fraction {W/W}': [x.initialHeatRecoveryCoolingCapacityFraction() for x in all_objects],
        'Heat Recovery Cooling Capacity Time Constant {hr}': [x.heatRecoveryCoolingCapacityTimeConstant() for x in all_objects],
        'Heat Recovery Cooling Energy Modifier Curve Name': [x.heatRecoveryCoolingEnergyModifierCurve().get().name() if not x.heatRecoveryCoolingEnergyModifierCurve().isNull() else None for x in all_objects],
        'Initial Heat Recovery Cooling Energy Fraction {W/W}': [x.initialHeatRecoveryCoolingEnergyFraction() for x in all_objects],
        'Heat Recovery Cooling Energy Time Constant {hr}': [x.heatRecoveryCoolingEnergyTimeConstant() for x in all_objects],
        'Heat Recovery Heating Capacity Modifier Curve Name': [x.heatRecoveryHeatingCapacityModifierCurve().get().name() if not x.heatRecoveryHeatingCapacityModifierCurve().isNull() else None for x in all_objects],
        'Initial Heat Recovery Heating Capacity Fraction {W/W}': [x.initialHeatRecoveryHeatingCapacityFraction() for x in all_objects],
        'Heat Recovery Heating Capacity Time Constant {hr}': [x.heatRecoveryHeatingCapacityTimeConstant() for x in all_objects],
        'Heat Recovery Heating Energy Modifier Curve Name': [x.heatRecoveryHeatingEnergyModifierCurve().get().name() if not x.heatRecoveryHeatingEnergyModifierCurve().isNull() else None for x in all_objects],
        'Initial Heat Recovery Heating Energy Fraction {W/W}': [x.initialHeatRecoveryHeatingEnergyFraction() for x in all_objects],
        'Heat Recovery Heating Energy Time Constant {hr}': [x.heatRecoveryHeatingEnergyTimeConstant() for x in all_objects]
    }

  # Create a DataFrame of Heat Exchanger Air To Air Sensible And Latent Objects.
    all_objects_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_objects_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} OS:AirConditioner:VariableRefrigerantFlow Objects")
    return all_objects_df

#-----------------------
#--- OS:Coil:Heating:Gas
#------------------------

def get_coil_heating_gas_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets an OS:Coil:Heating:Gas object information and returns it as a dictionary.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model containing the OS:Coil:Heating:Gas object.
        handle (str, optional): The handle of the OS:Coil:Heating:Gas object. Either handle or name must be provided.
        name (str, optional): The name of the OS:Coil:Heating:Gas object. Either name or handle must be provided.

    Returns:
        dict: A dictionary containing the OS:Coil:Heating:Gas object's properties, or an empty dictionary if not found.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getCoilHeatingGas(handle)
        if osm_object is None:
            print(
                f"No OS:Coil:Heating:Gas object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getCoilHeatingGasByName(name)
        if not osm_object:
            print(
                f"No OS:Coil:Heating:Gas object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
                  'Handle': str(target_object.handle()),
                  'Name': target_object.name().get() if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
                  'Gas Burner Efficiency': target_object.gasBurnerEfficiency(),
                  'Nominal Capacity {W}': target_object.nominalCapacity() if not target_object.isNominalCapacityAutosized() else 'Autosize',
                  'Air Inlet Node Name': None,
                  'Air Outlet Node Name': None,
                  'Temperature Setpoint Node Name': None,
                  'On Cycle Parasitic Electric Load {W}': target_object.onCycleParasiticElectricLoad(),
                  'Part Load Fraction Correlation Curve Name': None,
                  'Off Cycle Parasitic Gas Load {W}': target_object.offCycleParasiticGasLoad()                           
    }

    return object_dict

def get_all_coil_heating_gas_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Coil:Heating:Gas objects from the OpenStudio model 
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a OS:Coil:Heating:Gas object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getCoilHeatingGass()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_coil_heating_gas_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_coil_heating_gas_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Zone Coil Heating Gas objects from the OpenStudio model 
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all Coil Heating Gas objects.
    """

    all_objects_dicts = get_all_coil_heating_gas_objects_as_dicts(osm_model)

    # Create a DataFrame of all Coil Heating Gas objects.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} Coil Heating Gas objects")

    return all_objects_df

#---------------------------
#--- OOS:Coil:Heating:Water
#---------------------------
def get_coil_heating_water_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a single Coil Heating Water object from the OpenStudio model by handle or name.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    
    Returns:
    - dict: Dictionary containing information about the Coil Heating Water object.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getCoilHeatingWater(handle)
        if osm_object is None:
            print(
                f"No Sizing:System object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getCoilHeatingWaterByName(name)
        if not osm_object:
            print(
                f"No Sizing:System object found with the name: {name}")
            return {}

    target_object = osm_object.get()
    
       
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.nameString() if target_object.name().is_initialized() else None,
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'U-Factor Times Area Value {W/K}': float(target_object.uFactorTimesAreaValue()) if not target_object.isUFactorTimesAreaValueAutosized() else 'autosize',
        'Maximum Water Flow Rate {m3/s}': float(target_object.maximumWaterFlowRate()) if not target_object.isMaximumWaterFlowRateAutosized() else 'autosize',
        'Water Inlet Node Name': target_object.waterInletPort(),
        'Water Outlet Node Name': target_object.waterOutletPort(),
        'Air Inlet Node Name': target_object.airInletPort(),
        'Air Outlet Node Name': target_object.airOutletPort(),
        'Performance Input Method': target_object.performanceInputMethod(),
        'Rated Capacity {W}': float(target_object.ratedCapacity()) if not target_object.isRatedCapacityAutosized() else 'autosize',
        'Rated Inlet Water Temperature {C}': target_object.ratedInletWaterTemperature(),
        'Rated Inlet Air Temperature {C}': target_object.ratedInletAirTemperature(),
        'Rated Outlet Water Temperature {C}': target_object.ratedOutletWaterTemperature(),
        'Rated Outlet Air Temperature {C}': target_object.ratedOutletAirTemperature(),
        'Rated Ratio for Air and Water Convection': target_object.ratedRatioForAirAndWaterConvection()
        

    }        
    return object_dict

def get_all_coil_heating_water_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all Coil Heating Water objects from the OpenStudio model and return their attributes as a list of dictionaries.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    
    Returns:
    - list[dict]: A list of dictionaries, each containing information about a Coil Heating Water object.
    """
    
    all_objects = osm_model.getCoilHeatingWaters()
    all_objects_dicts = []
    
    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_coil_heating_water_object_as_dict(osm_model, handle=object_handle)
        if object_dict: 
            all_objects_dicts.append(object_dict)
            
    return all_objects_dicts

def get_all_coil_heating_water_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Coil Heating Water objects from the OpenStudio model and return their attributes as a pandas DataFrame.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    
    Returns:
    - pd.DataFrame: DataFrame containing information about all Coil Heating Water objects.
    """
    
    all_objects_dicts = get_all_coil_heating_water_objects_as_dicts(osm_model)
    
    all_objects_df = pd.DataFrame(all_objects_dicts)
    
    if not all_objects_df.empty and 'Name' in all_objects_df.columns:
        all_objects_df = all_objects_df.sort_values(
            by='Name', ascending=True, na_position='last'
        ).reset_index(drop=True)
    elif not all_objects_df.empty and 'Handle' in all_objects_df.columns:
        all_objects_df = all_objects_df.sort_values(
            by='Handle', ascending=True
        ).reset_index(drop=True)

    print(f"The OSM model contains {all_objects_df.shape[0]} Coil Heating Water objects")
    
    return all_objects_df

#---------------------------
#--- OOS:Coil:Cooling:Water
#---------------------------

def get_coil_cooling_water_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Retrieve a single Coil Cooling Water object from the OpenStudio model by handle or name.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    
    Returns:
    - dict: Dictionary containing information about the Coil Cooling Water object.
    """
    
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getCoilCoolingWater(handle)
        if osm_object is None:
            print(
                f"No Sizing:System object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getCoilCoolingWaterByName(name)
        if not osm_object:
            print(
                f"No Sizing:System object found with the name: {name}")
            return {}

    target_object = osm_object.get()
    
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.nameString() if target_object.name().is_initialized() else None,
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Design Water Flow Rate {m3/s}': target_object.designWaterFlowRate() if not target_object.isDesignWaterFlowRateAutosized() else 'autosize',
        'Design Air Flow Rate {m3/s}': target_object.designAirFlowRate() if not target_object.isDesignWaterFlowRateAutosized else 'autosize',
        'Design Inlet Water Temperature {C}': target_object.designInletWaterTemperature() if not target_object.isDesignWaterFlowRateAutosized else 'autosize',
        'Design Inlet Air Temperature {C}': target_object.designInletAirTemperature() if not target_object.isDesignWaterFlowRateAutosized else 'autosize',        
        'Design Outlet Air Temperature {C}': target_object.designOutletAirTemperature() if not target_object.isDesignWaterFlowRateAutosized else 'autosize',
        'Design Inlet Air Humidity Ratio {kg-H2O/kg-air}': target_object.designInletAirHumidityRatio() if not target_object.isDesignWaterFlowRateAutosized else 'autosize',
        'Design Outlet Air Humidity Ratio {kg-H2O/kg-air}': target_object.designOutletAirHumidityRatio() if not target_object.isDesignWaterFlowRateAutosized else 'autosize',
        'Water Inlet Node Name': target_object.waterInletPort(),
        'Water Outlet Node Name': target_object.waterOutletPort(),
        'Air Inlet Node Name': target_object.airInletPort(),
        'Air Outlet Node Name': target_object.airOutletPort(),
        'Type of Analysis': None,
        'Heat Exchanger Configuration': target_object.heatExchangerConfiguration()        
    }
    return object_dict 


def get_all_coil_cooling_water_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all Coil Cooling Water objects from the OpenStudio model and return their attributes as a list of dictionaries.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    
    Returns:
    - list[dict]: A list of dictionaries, each containing information about a Coil Cooling Water object.
    """
    
    all_coil_objects = osm_model.getCoilCoolingWaters()
    all_coil_dicts = []
    
    for coil_object in all_coil_objects:
        object_handle = str(coil_object.handle())
        coil_dict = get_coil_cooling_water_object_as_dict(osm_model, handle=object_handle)
        if coil_dict: 
            all_coil_dicts.append(coil_dict)
            
    return all_coil_dicts

def get_all_coil_cooling_water_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Coil Cooling Water objects from the OpenStudio model and return their attributes as a pandas DataFrame.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    
    Returns:
    - pd.DataFrame: DataFrame containing information about all Coil Cooling Water objects.
    """
    
    all_coil_dicts = get_all_coil_cooling_water_objects_as_dicts(osm_model)
    
    all_coil_df = pd.DataFrame(all_coil_dicts)
    
    if not all_coil_df.empty and 'Name' in all_coil_df.columns:
        all_coil_df = all_coil_df.sort_values(
            by='Name', ascending=True, na_position='last'
        ).reset_index(drop=True)
    elif not all_coil_df.empty and 'Handle' in all_coil_df.columns:
        all_coil_df = all_coil_df.sort_values(
            by='Handle', ascending=True
        ).reset_index(drop=True)

    print(f"The OSM model contains {all_coil_df.shape[0]} Coil Cooling Water objects")
    
    return all_coil_df


# --------------------------------------------------
#  ***** OS:Pump:VariableSpeed *********************
# --------------------------------------------------


def get_pump_variable_speed_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Pump:VariableSpeed object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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
        osm_object = osm_model.getPumpVariableSpeed(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getPumpVariableSpeedByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle': str(target_object.handle()), 
                   'Name': target_object.nameString() if target_object.name().is_initialized() else None, 
                   'Inlet Node Name': target_object.inletPort(), 
                   'Outlet Node Name': target_object.outletPort(), 
                   'Rated Flow Rate {m3/s}': target_object.ratedFlowRate().get() if target_object.ratedFlowRate().is_initialized() else None, 
                   'Rated Pump Head {Pa}': target_object.ratedPumpHead(), 
                   'Rated Power Consumption {W}': target_object.ratedPowerConsumption().get() if target_object.ratedPowerConsumption().is_initialized() else None,
                   'Motor Efficiency': target_object.motorEfficiency(), 
                   'Fraction of Motor Inefficiencies to Fluid Stream': target_object.fractionofMotorInefficienciestoFluidStream(), 
                   'Coefficient 1 of the Part Load Performance Curve': target_object.coefficient1ofthePartLoadPerformanceCurve(), 
                   'Coefficient 2 of the Part Load Performance Curve': target_object.coefficient2ofthePartLoadPerformanceCurve(), 
                   'Coefficient 3 of the Part Load Performance Curve': target_object.coefficient3ofthePartLoadPerformanceCurve(), 
                   'Coefficient 4 of the Part Load Performance Curve': target_object.coefficient4ofthePartLoadPerformanceCurve(), 
                   'Minimum Flow Rate {m3/s}': target_object.minimumFlowRate(), 
                   'Pump Control Type': target_object.pumpControlType(), 
                   'Pump Flow Rate Schedule Name': target_object.pumpFlowRateSchedule().nameString() if target_object.pumpFlowRateSchedule().is_initialized() else None, 
                   'Pump Curve Name': None, 
                   'Impeller Diameter {m}': None, 
                   'VFD Control Type': None, 
                   'Pump RPM Schedule Name': None, 
                   'Minimum Pressure Schedule {Pa}': None, 
                   'Maximum Pressure Schedule {Pa}': None, 
                   'Minimum RPM Schedule {rev/min}': None, 
                   'Maximum RPM Schedule {rev/min}': None, 
                   'Zone Name': None, 
                   'Skin Loss Radiative Fraction': target_object.skinLossRadiativeFraction(), 
                   'Design Power Sizing Method': target_object.designPowerSizingMethod(), 
                   'Design Electric Power per Unit Flow Rate {W/(m3/s)}': target_object.designElectricPowerPerUnitFlowRate(), 
                   'Design Shaft Power per Unit Flow Rate per Unit Head {W-s/m3-Pa}': target_object.designShaftPowerPerUnitFlowRatePerUnitHead(), 
                   'Design Minimum Flow Rate Fraction': target_object.designMinimumFlowRateFraction(), 
                   'End-Use Subcategory': target_object.endUseSubcategory()}

    return object_dict

def get_all_pump_variable_speed_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Pump:VariableSpeed objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a pump variable speed object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getPumpVariableSpeeds()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_pump_variable_speed_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_pump_variable_speed_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all pump variable speed objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all pump variable speed objects.
    """

    all_objects_dicts = get_all_pump_variable_speed_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Inlet Node Name', 'Outlet Node Name', 'Rated Flow Rate {m3/s}', 'Rated Pump Head {Pa}', 'Rated Power Consumption {W}', 'Motor Efficiency', 'Fraction of Motor Inefficiencies to Fluid Stream', 'Coefficient 1 of the Part Load Performance Curve', 'Coefficient 2 of the Part Load Performance Curve', 'Coefficient 3 of the Part Load Performance Curve', 'Coefficient 4 of the Part Load Performance Curve', 'Minimum Flow Rate {m3/s}', 'Pump Control Type', 'Pump Flow Rate Schedule Name', 'Pump Curve Name', 'Impeller Diameter {m}', 'VFD Control Type', 'Pump RPM Schedule Name', 'Minimum Pressure Schedule {Pa}', 'Maximum Pressure Schedule {Pa}', 'Minimum RPM Schedule {rev/min}', 'Maximum RPM Schedule {rev/min}', 'Zone Name', 'Skin Loss Radiative Fraction', 'Design Power Sizing Method', 'Design Electric Power per Unit Flow Rate {W/(m3/s)}', 'Design Shaft Power per Unit Flow Rate per Unit Head {W-s/m3-Pa}', 'Design Minimum Flow Rate Fraction', 'End-Use Subcategory']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all pump variable speed objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} pump variable speed objects.")

    return all_objects_df


# --------------------------------------------------
#  ***** OS:Chiller:Electric:EIR *******************
# --------------------------------------------------


def get_chiller_electric_eir_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    """
    Gets a specified OS:Chiller:Electric:EIR object from the OpenStudio model by either handle or name and return its attributes as a dictionary.

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
        osm_object = osm_model.getChillerElectricEIR(handle)
        if osm_object is None:
            print(f"No object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getChillerElectricEIRByName(name)
        if not osm_object:
            print(f"No object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    # Define attributes to retrieve in a dictionary
    object_dict = {'Handle': str(target_object.handle()), 
                   'Name': target_object.nameString(), 
                   'Reference Capacity {W}': target_object.referenceCapacity().get() if not target_object.isReferenceCapacityAutosized() else 'autosize', 
                   'Reference COP {W/W}': target_object.referenceCOP(), 
                   'Reference Leaving Chilled Water Temperature {C}': target_object.referenceLeavingChilledWaterTemperature(), 
                   'Reference Entering Condenser Fluid Temperature {C}': target_object.referenceEnteringCondenserFluidTemperature(), 
                   'Reference Chilled Water Flow Rate {m3/s}': target_object.referenceChilledWaterFlowRate().get() if not target_object.isReferenceChilledWaterFlowRateAutosized() else 'autosize', 
                   'Reference Condenser Fluid Flow Rate {m3/s}': target_object.referenceCondenserFluidFlowRate().get() if not target_object.isReferenceCondenserFluidFlowRateAutosized() else 'autosize', 
                   'Cooling Capacity Function of Temperature Curve Name': target_object.coolingCapacityFunctionOfTemperature().nameString(), 
                   'Electric Input to Cooling Output Ratio Function of Temperature Curve Name': target_object.electricInputToCoolingOutputRatioFunctionOfTemperature().nameString(),  
                   'Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name': target_object.electricInputToCoolingOutputRatioFunctionOfPLR().nameString(), 
                   'Minimum Part Load Ratio': target_object.minimumPartLoadRatio(), 
                   'Maximum Part Load Ratio': target_object.maximumPartLoadRatio(), 
                   'Optimum Part Load Ratio': target_object.optimumPartLoadRatio(), 
                   'Minimum Unloading Ratio': target_object.minimumUnloadingRatio(), 
                   'Chilled Water Inlet Node Name': target_object.supplyInletPort(), 
                   'Chilled Water Outlet Node Name': target_object.supplyOutletPort(), 
                   'Condenser Inlet Node Name': None, 
                   'Condenser Outlet Node Name': None, 
                   'Condenser Type': target_object.condenserType(), 
                   'Condenser Fan Power Ratio {W/W}': target_object.condenserFanPowerRatio(), 
                   'Fraction of Compressor Electric Consumption Rejected by Condenser': None, 
                   'Leaving Chilled Water Lower Temperature Limit {C}': target_object.leavingChilledWaterLowerTemperatureLimit(), 
                   'Chiller Flow Mode': target_object.chillerFlowMode(), 
                   'Design Heat Recovery Water Flow Rate {m3/s}': target_object.designHeatRecoveryWaterFlowRate().get() if not target_object.isDesignHeatRecoveryWaterFlowRateAutosized() else 'autosize', 
                   'Heat Recovery Inlet Node Name': None, 
                   'Heat Recovery Outlet Node Name': None, 
                   'Sizing Factor': target_object.sizingFactor(), 
                   'Basin Heater Capacity {W/K}': target_object.basinHeaterCapacity(), 
                   'Basin Heater Setpoint Temperature {C}': target_object.basinHeaterSetpointTemperature(), 
                   'Basin Heater Operating Schedule Name': target_object.basinHeaterSchedule().get() if target_object.basinHeaterSchedule().is_initialized() else None, 
                   'Condenser Heat Recovery Relative Capacity Fraction': target_object.condenserHeatRecoveryRelativeCapacityFraction(), 
                   'Heat Recovery Inlet High Temperature Limit Schedule Name': None, 
                   'Heat Recovery Leaving Temperature Setpoint Node Name': target_object.heatRecoveryLeavingTemperatureSetpointNode().get() if target_object.heatRecoveryLeavingTemperatureSetpointNode().is_initialized() else None, 
                   'End-Use Subcategory': target_object.endUseSubcategory()}

    return object_dict

def get_all_chiller_electric_eir_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Gets all OS:Chiller:Electric:EIR objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a chiller electric eir object.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getChillerElectricEIRs()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_chiller_electric_eir_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_chiller_electric_eir_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Gets all chiller electric eir objects from the OpenStudio model and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all chiller electric eir objects.
    """

    all_objects_dicts = get_all_chiller_electric_eir_objects_as_dicts(osm_model)

    # Define the columns for the DataFrame
    columns = ['Handle', 'Name', 'Reference Capacity {W}', 'Reference COP {W/W}', 'Reference Leaving Chilled Water Temperature {C}', 'Reference Entering Condenser Fluid Temperature {C}', 'Reference Chilled Water Flow Rate {m3/s}', 'Reference Condenser Fluid Flow Rate {m3/s}', 'Cooling Capacity Function of Temperature Curve Name', 'Electric Input to Cooling Output Ratio Function of Temperature Curve Name', 'Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name', 'Minimum Part Load Ratio', 'Maximum Part Load Ratio', 'Optimum Part Load Ratio', 'Minimum Unloading Ratio', 'Chilled Water Inlet Node Name', 'Chilled Water Outlet Node Name', 'Condenser Inlet Node Name', 'Condenser Outlet Node Name', 'Condenser Type', 'Condenser Fan Power Ratio {W/W}', 'Fraction of Compressor Electric Consumption Rejected by Condenser', 'Leaving Chilled Water Lower Temperature Limit {C}', 'Chiller Flow Mode', 'Design Heat Recovery Water Flow Rate {m3/s}', 'Heat Recovery Inlet Node Name', 'Heat Recovery Outlet Node Name', 'Sizing Factor', 'Basin Heater Capacity {W/K}', 'Basin Heater Setpoint Temperature {C}', 'Basin Heater Operating Schedule Name', 'Condenser Heat Recovery Relative Capacity Fraction', 'Heat Recovery Inlet High Temperature Limit Schedule Name', 'Heat Recovery Leaving Temperature Setpoint Node Name', 'End-Use Subcategory']

    # If all_objects_dicts is None or empty, create an empty DataFrame with the defined columns
    if not all_objects_dicts:
        all_objects_df = pd.DataFrame(columns=columns)
    else:
        # Create a DataFrame of all chiller electric eir objects.
        all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True, na_position='first').reset_index(drop=True)

    print(
        f"The OSM model contains {all_objects_df.shape[0]} chiller electric eir objects.")

    return all_objects_df