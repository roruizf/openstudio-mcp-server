# src/openstudio_toolkit/utils/notebook_helpers.py

import os
from typing import Tuple, Optional

def get_osm_path(
    use_gdrive: bool,
    gdrive_path: Optional[str] = None,
    local_path: Optional[str] = None
) -> Tuple[str, str]:
    """
    Handles file access for notebooks in both Colab and local environments.

    Args:
        use_gdrive (bool): In Colab, if True, uses Google Drive. If False, prompts for upload.
                           This argument is ignored in a local environment.
        gdrive_path (str, optional): The full path to the .osm file in Google Drive.
        local_path (str, optional): The full path to the .osm file on your local machine.

    Returns:
        Tuple[str, str]: A tuple containing:
            - The absolute path to the final .osm file.
            - The absolute path to the directory containing the file.
    """
    try:
        from google.colab import drive, files
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False

    if not IN_COLAB:
        # --- Local Environment Logic ---
        print("INFO: Running in a local environment.")
        if not local_path:
            raise ValueError("ERROR: 'local_path' must be provided when running locally.")
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"ERROR: File not found at local path: {local_path}")
        
        osm_file_path = os.path.abspath(local_path)
        project_folder_path = os.path.dirname(osm_file_path)
    else:
        # --- Colab Environment Logic ---
        if use_gdrive:
            if not gdrive_path: raise ValueError("'gdrive_path' is required when 'use_gdrive' is True.")
            print("INFO: Mounting Google Drive...")
            drive.mount('/content/drive', force_remount=True)
            if not os.path.exists(gdrive_path): raise FileNotFoundError(f"File not found in GDrive: {gdrive_path}")
            osm_file_path = gdrive_path
            project_folder_path = os.path.dirname(gdrive_path)
        else:
            print("INFO: Please use the button below to upload your .osm file.")
            project_folder_path = '/content'
            uploaded = files.upload()
            if not uploaded: raise FileNotFoundError("No file was uploaded.")
            file_name = next(iter(uploaded))
            osm_file_path = os.path.join(project_folder_path, file_name)

    print(f"✅ Success! Using model: {osm_file_path}")
    return osm_file_path, project_folder_path