from logger_config import log_args_kwargs as print
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional
import re
import shutil
from matplotlib import font_manager
from PIL import Image, ImageFont
from constants import *
from global_signals import global_signals
from paths import Paths
import os
import re
import shutil

def next_available_path(path):
    base, extension = os.path.splitext(path)
    i = 1
    while os.path.exists(path):
        path = f"{base} - alt {i}{extension}"
        i += 1
    return path

def clear_temp_folder(path = Paths.temp_templates):
    """
    Clears the temporary folder by deleting all files and subfolders.
    """
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)
    except Exception as e:
        print("Pi8kV", f"An error occurred while clearing the temp folder: {e}")

def duplicate_file(path):
    directory, filename = os.path.split(path)
    name, ext = os.path.splitext(filename)
    
    # Adjust the base filename to account for existing copy numbers in its name
    base_name_search = re.search(r"(.+)-copy\((\d+)\)", name)
    if base_name_search:
        name, current_copy_number = base_name_search.groups()
        current_copy_number = int(current_copy_number)
    else:
        current_copy_number = 0

    # Regular expression to match files with the same base name and a copy number
    regex = re.compile(rf"{re.escape(name)}-copy\((\d+)\){re.escape(ext)}$")
    
    # Find the highest copy number
    max_num = current_copy_number
    for f in os.listdir(directory):
        match = regex.match(f)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)
    
    # Generate new filename with incremented copy number
    new_filename = f"{name}-copy({max_num + 1}){ext}"
    new_path = os.path.join(directory, new_filename)
    
    # Copy the file
    shutil.copy(path, new_path)
    return new_path

def get_available_font(preferred_fonts, fallback_font_path):
    # Check if the fallback font exists
    if fallback_font_path is not None:
        if os.path.exists(fallback_font_path):
            return fallback_font_path

    # Get a list of available system fonts
    available_fonts = {
        font_manager.FontProperties(fname=font).get_name(): font
        for font in font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
    }

    # Attempt to find a preferred font
    for font_name in preferred_fonts:
        if font_name in available_fonts:
            return available_fonts[font_name]

    # As a last resort, use the first available system font
    if available_fonts:
        return next(iter(available_fonts.values()))

    raise FileNotFoundError("No suitable fonts found.")

def save_json_file(framework_data_dict, folder_path=Paths.frameworks_templates):
    """
    save json file in frameworks folder

    PARAMS
    framework_data_dict : dict : structure is :
    {"framework": {"width": 4500,"height": 5400},
    "image" : {"size": [4045,3300],"position": [227,1065],"layer": 1 },
    "texts" : [{"size": [4045,600],"position": [227,200],"layer": 2 },
                {"size": [4045,790],"position": [227,4400],"layer": 3 }],
    "icon_path" : "",
    "name" : "T3"
      }

    PS: the   "icon_path" key should be left an empty string as it will be filled automatically later

    """

    # Define default filename template
    default_filename_framework = "framework{}.json"

    # Check and extract 'name' key from dict, set to default if necessary
    name = framework_data_dict.get("name")
    if not isinstance(name, str) or name.strip() == "":
        # Find the highest numbered default file
        existing_defaults = [
            f
            for f in os.listdir(folder_path)
            if f.startswith("framework") and f.endswith(".json")
        ]
        highest_num = 0
        for file in existing_defaults:
            parts = file.replace("framework", "").replace(".json", "")
            if parts.isdigit():
                highest_num = max(highest_num, int(parts))
        name = default_filename_framework.format(highest_num + 1)
    else:
        name = f"{name}.json"

    # Ensure unique filename
    filename = os.path.join(folder_path, name)
    filename_without_ext = filename.replace(".json", "")
    counter = 1
    while os.path.exists(filename):
        filename = f"{filename_without_ext}_{counter}.json"
        counter += 1

    # Save dict to file
    with open(filename, "w") as file:
        json.dump(framework_data_dict, file, indent=4)

    global_signals.update_frameworks_scroll_area.emit()
    global_signals.update_templates_scroll_area.emit()

    return filename

def is_svg_file(file_path: str) -> bool:
    """
    Checks if the given file path points to a valid SVG file.
    """
    try:
        if file_path is None:
            return False
        if not os.path.exists(file_path):
            return False
        else:
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                return root.tag.endswith("svg")
            except ET.ParseError:
                print(f"This path doesn't return a valid SVG file: {file_path}")
                return False

    except TypeError:
        print("5Tul0", )

def verify_font_path(file_path: str) -> str:
    """
    Verifies if the given font path is valid and the font is loadable.
    """

    if not os.path.exists(file_path):
        print("00Y9O", f"File not found: {file_path}")
        return "arial"

    try:
        ImageFont.truetype(file_path, 10)
        return file_path
    except IOError:
        print("RC9U5", "Failed to load font.")
        return "arial"
 
def ensure_directory_exists_from_file_path(file_path: str) -> None:
    """
    Ensures the directory for the given file path exists.
    """
    print("WsPP7",f"Ensuring for this file path: {file_path}")
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
 
def unique_filename(file_path: str) -> str:
    """
    Generates a unique filename by appending a counter if the file already exists.
    """
    directory, filename = os.path.split(file_path)
    name, extension = os.path.splitext(filename)

    counter = 1
    while os.path.exists(file_path):
        if f"-{counter - 1}" in name:
            name = name.replace(f"-{counter - 1}", f"-{counter}")
        else:
            name = f"{name}-{counter}"

        file_path = os.path.join(directory, f"{name}{extension}")
        counter += 1

    return file_path

def is_image_file(file_path: str) -> bool:
    """
    Checks if the given file path points to an image.
    """
    try:
        if file_path is None:
            return False
        if not os.path.exists(file_path):
            return False
        else:
            try:
                Image.open(file_path)
                return True
            except Exception:
                print(f"This path doesn't return an image file: {file_path}")
                return False

    except TypeError:
        print("GCtwN", "Type error occurred.")
        return False
 
def get_images_paths_list_in_folder(folder_path: str) -> List[str]:
    """
    Returns a list of image paths in the given folder.
    """
    image_paths = []
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in IMAGE_EXTENSIONS:
                    image_paths.append(os.path.abspath(os.path.join(root, file)))
    except Exception as e:
        print("ahsTr", f"An error occurred while getting image paths: {e}")
    return image_paths

def get_font_paths_list_in_folder(folder_path: str) -> List[str]:
    """
    Returns a list of font paths in the given folder.
    """
    font_paths = []
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in FONT_EXTENSIONS:
                    font_paths.append(os.path.abspath(os.path.join(root, file)))
        if not font_paths:
            print(f"There are no fonts found in this folder: {folder_path}")
    except Exception as e:
        print("RSNR7", f"An error occurred while getting font paths: {e}")
    return font_paths

def get_filename_without_extension(file_path: str) -> str:
    """
    Returns the filename without extension.
    """
    return Path(file_path).stem
 
def get_filename_with_extension(file_path: str) -> str:
    """
    Returns the filename with extension.
    """
    return Path(file_path).name

def get_file_extension(file_path: str) -> str:
    """
    Returns the file extension of the given file path.
    """
    return Path(file_path).suffix

def get_folder_name(folder_path: str) -> Optional[str]:
    """
    Returns the folder name if the provided path is a directory.
    """
    path = Path(folder_path)
    try:
        if path.is_dir():
            return path.name
        else:
            print(f"The provided path is not a directory: {folder_path}")
            return None
    except Exception as e:
        print("5boaV", f"An error occurred while getting folder name: {e}")
        return None

