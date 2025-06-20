import requests
import json

def index_solr_docs(docs, SOLR_URL):
    headers = {"Content-Type": "application/json"}
    resp = requests.post(SOLR_URL, headers=headers, data=json.dumps(docs))
    if resp.status_code != 200:
        print(f"Unexpected Error {resp.status_code} - {resp.text}")

