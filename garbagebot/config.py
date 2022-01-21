"""
Handles the setting up of the config
"""
import yaml


def get_config(filename):
    """
    loads the yaml config and returns it as a dict
    """
    with open(filename, "r", encoding="UTF-8") as document:
        return yaml.safe_load(document)
