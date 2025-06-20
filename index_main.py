from orbit_utils.data_access import main_access
from orbit_utils.data_cleaning import clean_cols
from orbit_utils.create_solr_schema import FIELD_TYPES, add_field_type, FIELDS, add_field
from orbit_utils.index_orbit_sample import index_solr_docs
from orbit_utils.add_speelcheck import index_content
import pandas as pd
import json

SOLR_CORE_NAME = "orbit"
SOLR_URL_SCHEMA = f"http://localhost:8983/solr/{SOLR_CORE_NAME}/schema"
SOLR_URL_COMMIT = f"http://localhost:8983/solr/{SOLR_CORE_NAME}/update?commit=true"
SOLR_URL = f"http://localhost:8983/solr/{SOLR_CORE_NAME}"

def load_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    # 1. Aquisite data via arxiv and openalex APIs
    # main_access(r'data/arxiv_papers.jsonl', r'data/enriched_papers.jsonl') # Run Only for new data aquisation
    # solr_docs = pd.read_json(r'data/enriched_papers.jsonl', orient='records', lines=True)

    # 2. Clean and preprocess data
    # clean_cols(solr_docs, r'data/enriched_clean_papers.json')

    # 3. Cretae Index Schema
    for field_type in FIELD_TYPES:
        add_field_type(field_type, SOLR_URL_SCHEMA)

    for field in FIELDS:
        add_field(field, SOLR_URL_SCHEMA)

    # 4. Index Data
    solr_docs = load_data(r'data/enriched_clean_papers.json')   
    index_solr_docs(solr_docs, SOLR_URL_COMMIT)

    # 5. Add Spellcheck
    index_content(SOLR_URL)