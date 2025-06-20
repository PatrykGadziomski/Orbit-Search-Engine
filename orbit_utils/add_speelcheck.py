import requests
import json


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