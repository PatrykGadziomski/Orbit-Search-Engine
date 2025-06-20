"""
Author: Patryk Gadziomski
Updated: 20.06.2025
"""

import yaml
import os

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(os.path.join(current_dir, "..", "config.yml"))

    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    
    return config