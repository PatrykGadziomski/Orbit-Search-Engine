'''
Author: Patryk Gadziomski
Last udate: 27.07.2025
'''

import requests


FIELD_TYPES = [
    {
        "name": "string",
        "class": "solr.StrField",
        "sortMissingLast": True,
    },
    {
        "name": "boolean",
        "class": "solr.BoolField",
    },
    {
        "name": "pint",
        "class": "solr.IntPointField",
    },
    {
        "name": "date",
        "class": "solr.DatePointField", 
    },
    {
        "name": "text_general",
        "class": "solr.TextField",
        "positionIncrementGap": "100",
        "analyzer": {
            "tokenizer": {"class": "solr.StandardTokenizerFactory"},
            "filters": [{"class": "solr.LowerCaseFilterFactory"}],
        },
    },
    {
        "name": "text_custom",
        "class": "solr.TextField",
        "positionIncrementGap": "100",
        "indexAnalyzer": {
            "tokenizer": {"class": "solr.StandardTokenizerFactory"},
            "filters": [
                {"class": "solr.LowerCaseFilterFactory"},
                {"class": "solr.StopFilterFactory", "words": "stopwords.txt", "ignoreCase": "true"},
                {"class": "solr.PorterStemFilterFactory"}
            ]
        },
        "queryAnalyzer": {
            "tokenizer": {"class": "solr.StandardTokenizerFactory"},
            "filters": [
                {"class": "solr.LowerCaseFilterFactory"},
                {"class": "solr.StopFilterFactory", "words": "stopwords.txt", "ignoreCase": "true"},
                {"class": "solr.PorterStemFilterFactory"}
            ]
        }
    }    
]


FIELDS = [
    {"name": "arxiv_id", "type": "string", "stored": True, "indexed": True, "required": True},
    {"name": "openalex_id", "type": "string", "stored": True, "indexed": True, "required": True},
    {"name": "doi", "type": "string", "stored": True, "indexed": True, "required": False},
    {"name": "title", "type": "text_general", "stored": True, "indexed": True},
    {"name": "summary", "type": "text_general", "stored": True, "indexed": True, "multiValued": False},
    {"name": "published", "type": "date", "stored": True, "indexed": True, "docValues": True},
    {"name": "updated", "type": "date", "stored": True, "indexed": True, "docValues": True},
    {"name": "pdf_link", "type": "string", "stored": True, "indexed": True},
    {"name": "fulltext", "type": "text_custom", "stored": False, "indexed": True},
    {"name": "cited_by_count", "type": "pint", "stored": True, "indexed": False, "docValues": True},
    {"name": "type", "type": "string", "stored": True, "indexed": True, "docValues": True},
    {"name": "referenced_works", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "related_works", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "grants", "type": "string", "stored": True, "indexed": True, "docValues": True},
    {"name": "landing_page_url", "type": "string", "stored": True, "indexed": True},
    {"name": "author_orcid", "type": "string", "stored": True, "indexed": True, "multiValued": True},
    {"name": "volume", "type": "string", "stored": True, "indexed": True},
    {"name": "issue", "type": "string", "stored": True, "indexed": True},
    {"name": "first_page", "type": "string", "stored": True, "indexed": True},
    {"name": "last_page", "type": "string", "stored": True, "indexed": True},
    {"name": "journal", "type": "string", "stored": True, "indexed": True, "multiValued": "true", "docValues": True},
    {"name": "concepts", "type": "string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "author_names", "type": "text_general", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "open_access", "type": "boolean", "stored": True, "indexed": False, "multiValued": False, "docValues": True},
    {"name": "language", "type": "string", "stored": True, "indexed": True, "multiValued": True,"docValues": True},
    {"name": "keywords", "type": "string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "spellcheck_base", "type": "text_general", "stored": False, "indexed": True, "multiValued": True}
]


def add_field_type(type_def, SOLR_URL):   
    delete_payload = {"delete-field-type": {"name": type_def["name"]}}
    delete_response = requests.post(SOLR_URL, json=delete_payload)
    if delete_response.status_code == 200:
        print(f"Fieldtype '{type_def['name']}' deleted successfully.")
    
    payload = {"add-field-type": type_def}
    response = requests.post(SOLR_URL, json=payload)
    if response.status_code == 200:
        print(f"Fieldtype '{type_def['name']}' added successfully.")
    elif "already exists" in response.text:
        print(f"Fieldtype '{type_def['name']}' already exists.")
    else:
        print(f"Error during Fieldtype '{type_def['name']}': {response.text}")


def add_field(field_def, SOLR_URL):
    payload = {"add-field": field_def}
    response = requests.post(SOLR_URL, json=payload)
    if response.status_code == 200:
        print(f"Index-Field '{field_def['name']}' added to schema successfully.")
    elif "already exists" in response.text:
        print(f"Index-Field '{field_def['name']}' already exists.")
    else:
        print(f"Error during Field '{field_def['name']}': {response.text}")
