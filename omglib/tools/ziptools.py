import zipfile
from pathlib import Path

def extract_folder_from_zip(zip_file_path: str, folder_in_zip: str, output_folder: str):
    """
    Extracts all files from a specific folder inside a zip archive to another folder.
    
    Parameters:
        zip_file_path (str): Path to the zip file.
        folder_in_zip (str): The folder inside the zip file to extract.
        output_folder (str): The destination folder for extracted files.
    """
    zip_path = Path(zip_file_path)
    output_path = Path(output_folder)
    
    # Ensure the zip file exists
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file '{zip_file_path}' not found.")
    
    # Ensure the output folder exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # Iterate through the files in the zip file
        for file in zip_file.namelist():
            # Check if the file is within the specified folder
            if file.startswith(f"{folder_in_zip}/") and not file.endswith('/'):  # Skip directories
                # Extract file to the output folder
                destination = output_path / Path(file).name
                with zip_file.open(file) as source, open(destination, "wb") as target:
                    target.write(source.read())
                print(f"Extracted: {file} to {destination}")