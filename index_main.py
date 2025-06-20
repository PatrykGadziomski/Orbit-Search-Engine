"""
Author: Patryk Gadziomski
Updated: 20.06.2025
"""

from orbit_utils.data_access import main_access
from orbit_utils.data_cleaning import clean_cols
from orbit_utils.create_solr_schema import FIELD_TYPES, add_field_type, FIELDS, add_field
from orbit_utils.index_orbit import index_solr_docs
from orbit_utils.orbit_config_loader import load_config
import pandas as pd
import json

config = load_config()

SOLR_CORE_NAME = config['solr_core']
SOLR_PORT = config['solr_port']
SOLR_HOST = config['solr_host']

SOLR_URL_SCHEMA = f"http://{SOLR_HOST}:{SOLR_PORT}/solr/{SOLR_CORE_NAME}/schema"
SOLR_URL_COMMIT = f"http://{SOLR_HOST}:{SOLR_PORT}/solr/{SOLR_CORE_NAME}/update?commit=true"
SOLR_URL = f"http://{SOLR_HOST}:{SOLR_PORT}/solr/{SOLR_CORE_NAME}"

arxiv_path = config['arxiv_path']
arxiv_openalex_path = config['arxiv_openalex_path']
arxiv_openalex_clean_path = config['arxiv_openalex_clean_path']


def load_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    ### -- !!! The data download can take a while !!! -- Please use the data in ./data/ for first tests
    # 1. Aquisite data via arxiv and openalex APIs
    main_access(arxiv_path, arxiv_openalex_path) # Run Only for new data aquisition

    # 2. Clean and preprocess data
    solr_docs = pd.read_json(arxiv_openalex_path, orient='records', lines=True)
    clean_cols(solr_docs, arxiv_openalex_clean_path)

    # 3. Cretae Index Schema
    for field_type in FIELD_TYPES:
        add_field_type(field_type, SOLR_URL_SCHEMA)

    for field in FIELDS:
        add_field(field, SOLR_URL_SCHEMA)

    # 4. Index Data
    solr_docs = load_data(arxiv_openalex_clean_path)   
    index_solr_docs(solr_docs, SOLR_URL_COMMIT)
