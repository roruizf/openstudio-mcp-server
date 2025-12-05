import re
import pandas as pd
from typing import Union

def extract_table_by_name_from_energyplus_results_html(html_file_path: str, table_name: str) -> Union[pd.DataFrame, str, None]:
    """
    Reads an EnergyPlus results HTML file, finds the table immediately following the
    specified table name (enclosed within <b> tags), and extracts it as a pandas DataFrame.

    Args:
        html_file_path (str): The path to the EnergyPlus results HTML file.
        table_name (str): The exact text name of the table as it appears in the
                           EnergyPlus HTML file (e.g., 'Zone Sensible Cooling').
                           The function will search for this name enclosed within <b> tags.

    Returns:
        pandas.DataFrame or str or None: The extracted table as a DataFrame,
                                        an error message (str) if the table is not found,
                                        or None if some unexpected error occurs.
    """
    table_label = f'<b>{table_name}</b>'

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        return "Error: HTML file not found at the specified path."

    # Find the position after the specified table name (within <b> tags)
    start_index = html_content.find(table_label)
    if start_index == -1:
        return f"Error: Table with name '{table_name}' not found in the HTML."
    start_index += len(table_label) # Move past the label
    start_index = html_content.find('<table', start_index)
    if start_index == -1:
        return f"Error: Table not found immediately after '{table_name}'."

    # Find the end of the table
    end_index = html_content.find('</table>', start_index)
    if end_index == -1:
        return "Error: Closing '</table>' tag not found."

    table_html = html_content[start_index:end_index + len('</table>')]

    # Extract table rows
    rows = re.findall(r'<tr.*?>(.*?)</tr>', table_html, re.DOTALL)
    if not rows:
        return "Error: No rows found in the table."

    data = []
    headers = []
    for i, row_html in enumerate(rows):
        # Extract cells, handling both th (header) and td (data)
        cells = re.findall(r'<(th|td).*?>(.*?)</\1>', row_html, re.DOTALL)
        row_data = [cell[1].strip() for cell in cells]
        if i == 0:
            headers = row_data
        elif row_data:
            data.append(row_data)

    if not data:
        return "Error: No data found in the table."

    df = pd.DataFrame(data, columns=headers if headers else None)
    return df