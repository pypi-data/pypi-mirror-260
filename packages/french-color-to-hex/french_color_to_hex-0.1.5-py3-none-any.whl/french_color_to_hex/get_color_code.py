import json

def create_color_map(file_path='colors.json'):
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
