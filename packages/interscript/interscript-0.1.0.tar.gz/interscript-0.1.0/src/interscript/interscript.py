__all__ = ["map_exist", "map_list", "functions", "stdlib", "load_map", "transliterate"]

import importlib.util
import os

from . import functions as functions
from . import stdlib as stdlib

maps = stdlib.maps

def map_exist(map):
    return map in maps.keys()

def map_list(map):
    return maps.keys()

def load_map(map_name):
    if map_exist(map_name):
        return

    # Construct the path to the map file based on the map_name argument
    maps_dir = os.path.join(os.path.dirname(__file__), 'maps')
    map_file_path = os.path.join(maps_dir, f"{map_name}.py")

    # Check if the map file exists
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"No map file found for {map_name}")

    # Load the module
    spec = importlib.util.spec_from_file_location(map_name, map_file_path)
    map_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(map_module)

def transliterate(map, str, stage="main"):
    return maps[map]["stages"][stage](str)

