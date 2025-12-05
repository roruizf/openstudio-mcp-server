import os
from typing import Optional
import openstudio


def load_osm_file_as_model(osm_file_path: str, version_translator: Optional[bool] = True) -> openstudio.model.Model:
    """Loads an OSM file into an OpenStudio model.

    Args:
        osm_file_path: The path to the OSM file. This can be a relative path
            or an absolute path.
        version_translator: Whether to use the OpenStudio version translator.
            This is necessary if the OSM file is in a version of OpenStudio
            that is different from the version of OpenStudio that is being used
            to load the file. Defaults to True.

    Returns:
        An OpenStudio model containing the data from the OSM file.
    """
    # Get the absolute path to the OSM file.
    osm_file_path = os.path.abspath(osm_file_path)

    if version_translator:
        translator = openstudio.osversion.VersionTranslator()
        osm_model = translator.loadModel(osm_file_path).get()
    else:
        osm_model = openstudio.model.Model.load(osm_file_path).get()

    print(
        f"The OSM read file contains data for the {osm_model.building().get().name()}")
    # Return the OpenStudio model.
    return osm_model


def save_model_as_osm_file(osm_model: openstudio.model.Model, osm_file_path: str, new_file_name: Optional[str] = None) -> None:
    """
    Saves an OpenStudio model to a specified OSM file path.

    Args:
        osm_model: An OpenStudio model to be saved.
        osm_file_path: The path where the OSM file will be saved.
        new_file_name: An optional name for the new OSM file.

    Returns:
        None
    """
    # Extract the folder from the provided OSM file path.
    osm_file_folder = os.path.split(osm_file_path)[0]

    # Determine the new OSM file name if not specified.
    if new_file_name is not None:
        new_osm_file_name = new_file_name
    else:
        new_osm_file_name = os.path.split(osm_file_path)[-1]

    # Save the model to the new OSM file.    
    osm_model.save(os.path.join(osm_file_folder, new_osm_file_name), overwrite=True)


def convert_osm_to_idf(osm_model: openstudio.model.Model, idf_file_path: str) -> None:
    """
    Converts an OpenStudio model to an EnergyPlus IDF file.

    Args:
        osm_model: The OpenStudio model to be converted.
        idf_file_path: The path where the IDF file will be saved.

    Returns:
        None: This function saves the IDF file to the specified path.
    """
    # Create a ForwardTranslator to convert the model to IDF
    ft = openstudio.energyplus.ForwardTranslator()

    # Translate the OpenStudio model to an EnergyPlus model (IDF)
    idf_model = ft.translateModel(osm_model)

    # Save the translated model as an IDF file
    idf_model.save(idf_file_path, True)

    print(f"IDF file created successfully at: {idf_file_path}")
