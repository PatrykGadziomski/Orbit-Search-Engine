"""
Author: Patryk Gadziomski
Updated: 20.06.2025
"""

import requests

def index_solr_docs(docs, SOLR_URL):
    enriched_docs = []
    for doc in docs:
        title = doc.get("title", "")
        summary = doc.get("summary", "")
        fulltext = doc.get("full_text", "")
        
        doc["spellcheck_base"] = [title, summary, fulltext]

        if "id" not in doc and "arxiv_id" in doc:
            doc["id"] = doc["arxiv_id"]

        enriched_docs.append(doc)

    headers = {"Content-Type": "application/json"}
    resp = requests.post(f"{SOLR_URL}/update?commit=true", headers=headers, json=enriched_docs)

    if resp.status_code != 200:
        print(f"Unexpected Error {resp.status_code} - {resp.text}")
    else:
        print(f"{len(enriched_docs)} Dokumente erfolgreich indexiert.")
