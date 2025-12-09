# src/openstudio_toolkit/tasks/simulation_setup/set_output_variables.py

import openstudio
from typing import Dict, List, Literal

def validator(
    osm_model: openstudio.model.Model,
    variable_names: List[str],
    reporting_frequency: str
) -> Dict[str, List[str]]:
    """
    Validates that the inputs for setting output variables are correct.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model object.
        variable_names (List[str]): The list of variable names to add.
        reporting_frequency (str): The frequency to report.

    Returns:
        Dict[str, List[str]]: A dictionary with validation status and messages.
    """
    messages = []
    
    if not variable_names:
        return {"status": "ERROR", "messages": ["ERROR: The 'variable_names' list cannot be empty."]}

    # --- LIST OF VALID FREQUENCIES ---
    valid_frequencies = ["Detailed", "Timestep", "Hourly", "Daily", "Monthly", "RunPeriod", "Annual"]
    if reporting_frequency not in valid_frequencies:
        return {"status": "ERROR", "messages": [f"ERROR: '{reporting_frequency}' is not a valid reporting frequency. Choose from: {valid_frequencies}"]}

    messages.append(f"OK: Ready to set {len(variable_names)} output variables with '{reporting_frequency}' frequency.")
    return {"status": "READY", "messages": messages}

def run(
    osm_model: openstudio.model.Model,
    variable_names: List[str],    
    reporting_frequency: Literal["Detailed", "Timestep", "Hourly", "Daily", "Monthly", "RunPeriod", "Annual"],
    key_value: str = "*",
    remove_existing: bool = False
) -> openstudio.model.Model:
    """
    Sets Output:Variable objects in the OpenStudio model for simulation.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model to modify.
        variable_names (List[str]): A list of the output variable names to add.
        reporting_frequency (str): The reporting frequency.
        key_value (str, optional): The key value to filter results. Defaults to "*".
        remove_existing (bool, optional): If True, all existing Output:Variable objects
                                          will be removed. Defaults to False.

    Returns:
        openstudio.model.Model: The modified OpenStudio model object.
    """
    print("INFO: Starting 'Set Output Variables' task...")
    
    if remove_existing:
        existing_vars = osm_model.getOutputVariables()
        print(f"INFO: 'remove_existing' is True. Removing {len(existing_vars)} existing output variables.")
        for var in existing_vars:
            var.remove()

    added_count = 0
    for var_name in variable_names:
        output_var = openstudio.model.OutputVariable(var_name, osm_model)
        output_var.setKeyValue(key_value)
        output_var.setReportingFrequency(reporting_frequency)
        added_count += 1
        
    print(f"INFO: Task finished. {added_count} new output variables were set.")
    return osm_model