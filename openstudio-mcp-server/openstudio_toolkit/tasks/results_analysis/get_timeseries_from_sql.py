# src/openstudio_toolkit/tasks/results_analysis/get_timeseries_from_sql.py

import os
import sqlite3
import pandas as pd
from collections import OrderedDict, namedtuple
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# --- Internal Data Structures and Constants ---
# Re-define the Variable namedtuple for clarity within this module
Variable = namedtuple("Variable", "key type units")

# Define frequency constants
TS = "timestep"
H = "hourly"
D = "daily"
M = "monthly"
A = "annual"
RP = "runperiod"

# --- Internal Helper Functions (Logic from your provided code) ---

def _to_sql_frequency(eso_frequency: str) -> Optional[str]:
    """Converts short frequency names to SQL-compatible names."""
    frequencies = {
        TS: "Zone Timestep", H: "Hourly", D: "Daily",
        M: "Monthly", RP: "Run Period", A: "Annual"
    }
    return frequencies.get(eso_frequency)

def _eso_to_sql_variable(variable: Variable) -> Dict[str, str]:
    """Converts a Variable namedtuple to a dictionary for SQL queries."""
    sql_columns = ["KeyValue", "Name", "Units"]
    return {col: val for val, col in zip(variable, sql_columns) if val is not None}

def _data_dict_statement(columns: List[str], alike: bool) -> str:
    """Creates the SELECT statement for the ReportDataDictionary table."""
    statement = "SELECT ReportDataDictionaryIndex, KeyValue, Name, Units FROM ReportDataDictionary WHERE ReportingFrequency = ?"
    eq_operator = " LIKE ?" if alike else " = ?"
    conditions = [f"{column}{eq_operator}" for column in columns]
    if conditions:
        statement += " AND " + " AND ".join(conditions)
    return statement

def _fetch_data_dict_rows(conn, variable, sql_frequency, alike):
    """Executes the SQL query to find matching time series."""
    sql_variable = _eso_to_sql_variable(variable)
    statement = _data_dict_statement(list(sql_variable.keys()), alike)
    
    values = tuple(f"%{v}%" for v in sql_variable.values()) if alike else tuple(sql_variable.values())
    params = (sql_frequency,) + values
    
    return conn.execute(statement, params)

def _get_outputs(conn, id_: int) -> List[float]:
    """Gets all numerical values for a given time series ID."""
    statement = "SELECT Value FROM ReportData WHERE ReportDataDictionaryIndex = ?"
    return [r[0] for r in conn.execute(statement, (id_,))]

def _get_timestamps(conn, frequency: str) -> List[datetime]:
    """Gets all timestamps for a given frequency."""
    freq_map = {TS: -1, H: 1, D: 2, M: 3, RP: 4, A: 5}
    statement = f"SELECT Year, Month, Day, Hour, Minute FROM Time WHERE IntervalType = {freq_map[frequency.lower()]}"
    
    timestamps = []
    for year, month, day, hour, minute in conn.execute(statement):
        year = 2002 if year == 0 else year # Default year if not specified
        if hour == 24:
            timestamp = datetime(year, month, day) + timedelta(days=1)
        else:
            timestamp = datetime(year, month, day, hour, minute)
        timestamps.append(timestamp)
    return timestamps

# --- Main Task Functions ---

def validator(sql_path: str) -> Dict[str, List[str]]:
    """Validates that the SQL file path is valid."""
    if not os.path.exists(sql_path):
        return {"status": "ERROR", "messages": [f"ERROR: SQL file not found at: {sql_path}"]}
    
    # Quick check to see if it's a valid sqlite file with a key table
    try:
        conn = sqlite3.connect(sql_path)
        conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ReportData';").fetchone()
        conn.close()
    except sqlite3.DatabaseError:
        return {"status": "ERROR", "messages": [f"ERROR: The file at {sql_path} is not a valid SQLite database."]}

    return {"status": "READY", "messages": [f"OK: SQL file found and appears valid."]}

def run(
    sql_path: str,
    variables: List[Variable],
    frequency: str,
    alike: bool = False,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
    ) -> Optional[pd.DataFrame]:
    """
    Extracts specified time series data from an EnergyPlus SQL file into a pandas DataFrame,
    with an optional date range filter.

    Args:
        sql_path (str): The path to the EnergyPlus eplusout.sql file.
        variables (List[Variable]): A list of Variable namedtuples to query.
        frequency (str): The reporting frequency (e.g., 'hourly', 'daily').
        alike (bool, optional): If True, performs a partial (LIKE) match. Defaults to False.
        start_date (Optional[datetime], optional): The start date for filtering results. Defaults to None.
        end_date (Optional[datetime], optional): The end date for filtering results. Defaults to None.

    Returns:
        Optional[pd.DataFrame]: A DataFrame with a datetime index and columns for each
                                matching time series, or None if no data is found.
    """
    print(f"INFO: Starting 'Get Timeseries from SQL' task for '{frequency}' data...")
    conn = sqlite3.connect(sql_path)
    sql_frequency = _to_sql_frequency(frequency)
    
    results_data = {}
    
    for var_request in variables:
        rows = _fetch_data_dict_rows(conn, var_request, sql_frequency, alike)
        for id_, key, name, units in rows:
            column_name = f"{key}|{name}|{units}"
            results_data[column_name] = _get_outputs(conn, id_)

    if not results_data:
        print("WARNING: No matching time series were found for the given criteria.")
        conn.close()
        return None
        
    timestamps = _get_timestamps(conn, frequency)
    conn.close()
    
    # Ensure all data series have the same length as the timestamps
    min_len = min(len(timestamps), min(len(v) for v in results_data.values()))
    
    df = pd.DataFrame({k: v[:min_len] for k, v in results_data.items()})
    df.index = timestamps[:min_len]
    
    # Filter the final DataFrame by the date range if provided
    if start_date:
        df = df[df.index >= start_date]
    if end_date:
        df = df[df.index <= end_date]

    if df.empty:
        print("WARNING: No data remains after applying the date filter.")
        return None
    
    print(f"INFO: Task finished. Successfully extracted {len(df.columns)} time series within the specified date range.")
    return df