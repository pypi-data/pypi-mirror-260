import json
import os

def create_color_map(file_path=None):
    if file_path is None:
        # Get the path to the current module's directory
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'colors.json')

    # Read the JSON data from the file
    with open(file_path, 'r') as f:
        colors = json.load(f)

    # Create a dictionary mapping color names to color codes
    color_map = {color['nom'].lower(): color['code'] for color in colors}

    return color_map
def get_color_code(nom):
    color_map = create_color_map()
    code = color_map.get(nom.lower())
    return code
