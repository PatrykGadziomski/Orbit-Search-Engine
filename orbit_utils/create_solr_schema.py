"""
Author: Patryk Gadziomski
Updated: 20.06.2025
"""

import requests


FIELD_TYPES = [
    {
        "name": "orbit_string",
        "class": "solr.StrField",
        "sortMissingLast": True,
    },
    {
        "name": "orbit_boolean",
        "class": "solr.BoolField",
    },
    {
        "name": "orbit_pint",
        "class": "solr.IntPointField",
    },
    {
        "name": "orbit_date",
        "class": "solr.DatePointField", 
    },
    {
        "name": "orbit_text_general",
        "class": "solr.TextField",
        "positionIncrementGap": "100", # verhindert, dass multiValued-Feldwerte wie ein einziger Textblock behandelt werden
        "analyzer": {
            "tokenizer": {"class": "solr.StandardTokenizerFactory"},
            "filters": [{"class": "solr.LowerCaseFilterFactory"}],
        },
    },
    {
        "name": "orbit_text_custom",
        "class": "solr.TextField",
        "positionIncrementGap": "100", # verhindert, dass multiValued-Feldwerte wie ein einziger Textblock behandelt werden
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
    {"name": "arxiv_id", "type": "orbit_string", "stored": True, "indexed": True, "required": True},
    {"name": "openalex_id", "type": "orbit_string", "stored": True, "indexed": True, "required": True},
    {"name": "doi", "type": "orbit_string", "stored": True, "indexed": True, "required": False},
    {"name": "title", "type": "orbit_text_general", "stored": True, "indexed": True},
    {"name": "summary", "type": "orbit_text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "published", "type": "orbit_date", "stored": True, "indexed": True, "docValues": True},
    {"name": "updated", "type": "orbit_date", "stored": True, "indexed": True, "docValues": True},
    {"name": "pdf_link", "type": "orbit_string", "stored": True, "indexed": True},
    {"name": "fulltext", "type": "orbit_text_custom", "stored": False, "indexed": True},
    {"name": "cited_by_count", "type": "orbit_pint", "stored": True, "indexed": False, "docValues": True},
    {"name": "type", "type": "orbit_string", "stored": True, "indexed": True, "docValues": True},
    {"name": "referenced_works", "type": "orbit_text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "related_works", "type": "orbit_text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "grants", "type": "orbit_string", "stored": True, "indexed": True, "docValues": True},
    {"name": "landing_page_url", "type": "orbit_text_general", "stored": True, "indexed": True},
    {"name": "author_orcid", "type": "orbit_text_general", "stored": True, "indexed": True, "multiValued": True},
    {"name": "volume", "type": "orbit_string", "stored": True, "indexed": True},
    {"name": "issue", "type": "orbit_string", "stored": True, "indexed": True},
    {"name": "first_page", "type": "orbit_string", "stored": True, "indexed": True},
    {"name": "last_page", "type": "orbit_string", "stored": True, "indexed": True},

    {"name": "journal", "type": "orbit_string", "stored": True, "indexed": True, "multiValued": "true", "docValues": True},
    {"name": "concepts", "type": "orbit_string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "author_names", "type": "orbit_string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "open_access", "type": "orbit_boolean", "stored": True, "indexed": False, "multiValued": True, "docValues": True},
    {"name": "language", "type": "orbit_string", "stored": True, "indexed": True, "multiValued": True,"docValues": True},
    {"name": "institutions", "type": "orbit_string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},
    {"name": "keywords", "type": "orbit_string", "stored": True, "indexed": True, "multiValued": True, "docValues": True},

    {"name": "spellcheck_base", "type": "orbit_text_general", "stored": False, "indexed": True, "multiValued": True}
]

def add_field_type(type_def, SOLR_URL):
    # vorhandene Feldtypen können nicht überschrieben werden, daher
    # zuerst den Feldtyp löschen, falls er existiert    
    delete_payload = {"delete-field-type": {"name": type_def["name"]}}
    delete_response = requests.post(SOLR_URL, json=delete_payload)
    if delete_response.status_code == 200:
        print(f"Feldtyp '{type_def['name']}' erfolgreich gelöscht.")
    
    # jetzt können wir den Feldtyp hinzufügen
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

