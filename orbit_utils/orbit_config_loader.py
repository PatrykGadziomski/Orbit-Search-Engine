"""
Author: Patryk Gadziomski
Updated: 20.06.2025
"""

import yaml

def load_config(path: str="config.yaml") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading the config file: {e}")
        raise
