"""
Author: Patryk Gadziomski
Updated: 20.06.2025
"""

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
                {"class": "solr.StopFilterFactory", "words": "stopwords.txt", "ignoreCase": "true"}
            ]
        }
    }    
]


FIELDS = [
    {"name": "arxiv_id", "type": "string", "stored": True, "indexed": True, "required": True},
    {"name": "openalex_id", "type": "string", "stored": True, "indexed": True, "required": True},
    {"name": "doi", "type": "string", "stored": True, "indexed": True, "required": False},
    {"name": "title", "type": "text_general", "stored": True, "indexed": True},
    {"name": "summary", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "published", "type": "date", "stored": True, "indexed": True, "docValues": True},
    {"name": "updated", "type": "date", "stored": True, "indexed": True, "docValues": True},
    {"name": "pdf_link", "type": "string", "stored": True, "indexed": True},
    {"name": "fulltext", "type": "text_custom", "stored": False, "indexed": True},
    {"name": "cited_by_count", "type": "pint", "stored": True, "indexed": False, "docValues": True},
    {"name": "type", "type": "string", "stored": True, "indexed": True, "docValues": True},
    {"name": "referenced_works", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "related_works", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "grants", "type": "string", "stored": True, "indexed": True, "docValues": True},
    {"name": "landing_page_url", "type": "text_general", "stored": True, "indexed": True},
    {"name": "author_orcid", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "volume", "type": "string", "stored": True, "indexed": True},
    {"name": "issue", "type": "string", "stored": True, "indexed": True},
    {"name": "first_page", "type": "string", "stored": True, "indexed": True},
    {"name": "last_page", "type": "string", "stored": True, "indexed": True},
    {"name": "journal", "type": "string", "stored": True, "indexed": True, "multiValued": "true", "docValues": True},
    {"name": "concepts", "type": "string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "author_names", "type": "string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "open_access", "type": "boolean", "stored": True, "indexed": False, "multiValued": True, "docValues": True},
    {"name": "language", "type": "string", "stored": True, "indexed": True, "multiValued": True,"docValues": True},
    {"name": "institutions", "type": "string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "keywords", "type": "string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "spellcheck_base", "type": "text_general", "stored": False, "indexed": True, "multiValued": True}
]

def add_field_type(type_def, SOLR_URL):   
    delete_payload = {"delete-field-type": {"name": type_def["name"]}}
    delete_response = requests.post(SOLR_URL, json=delete_payload)
    if delete_response.status_code == 200:
        print(f"Feldtyp '{type_def['name']}' erfolgreich gelöscht.")
    
    payload = {"add-field-type": type_def}
    response = requests.post(SOLR_URL, json=payload)
    if response.status_code == 200:
        print(f"Feldtyp '{type_def['name']}' erfolgreich hinzugefügt.")
    elif "already exists" in response.text:
        print(f"Feldtyp '{type_def['name']}' existiert bereits.")
    else:
        print(f"Fehler bei Feldtyp '{type_def['name']}': {response.text}")


def add_field(field_def, SOLR_URL):
    payload = {"add-field": field_def}
    response = requests.post(SOLR_URL, json=payload)
    if response.status_code == 200:
        print(f"Index-Feld '{field_def['name']}' erfolgreich zum Schema hinzugefügt.")
    elif "already exists" in response.text:
        print(f"Index-Feld '{field_def['name']}' existiert bereits.")
    else:
        print(f"Fehler bei Feld '{field_def['name']}': {response.text}")
