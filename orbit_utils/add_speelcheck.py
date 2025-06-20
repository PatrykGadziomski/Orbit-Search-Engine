import requests
import json

# def add_spellcheck_field(SOLR_URL):
#     payload = {
#         "add-field": {
#             "name": "spellcheck_base",
#             "type": "orbit_text_general",
#             "stored": False,
#             "indexed": True,
#             "multiValued": True
#         }
#     }
#     response = requests.post(f"{SOLR_URL}/schema/fieldtypes", json=payload)
#     if response.status_code == 200:
#         print(f"Indexfeld 'spellcheck_base' erfolgreich hinzugefügt.")
#     else:
#         print(f"Fehler beim Hinzufügen des Indexfelds 'spellcheck_base': {response.status_code} - {response.text}")


def index_content(SOLR_URL):

    with open(r'data/enriched_clean_papers.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)

        for file in data:
            fulltext = file['full_text']
            arxiv_id = file['arxiv_id']
            openalex_id = file['openalex_id']
            title = file['title']
            summary = file['summary']
            published = file['published']
            cited_by_count = file['cited_by_count']
            
            doc = {
                "id": arxiv_id,
                "arxiv_id": arxiv_id,
                "openalex_id": openalex_id,
                "title": title,
                "summary": summary,
                "published": published,
                "cited_by_count": cited_by_count,
                "spellcheck_base": {
                    "set": [
                        title,
                        summary,
                        fulltext
                    ]
                }
            }
            headers = { "Content-Type": "application/json" }
            resp = requests.post(f"{SOLR_URL}/update?commit=true", headers=headers, json=[doc])
            if resp.status_code == 200:
                print(f"Solr-Dokument mit ID {arxiv_id} erfolgreich aktualisiert.")
            else:
                print(f"Fehler bei Solr-Update für Dokument mit ID {arxiv_id}: {resp.text}")