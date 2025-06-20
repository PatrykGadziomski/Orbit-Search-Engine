from flask import Flask, request, render_template
from orbit_utils.orbit_config_loader import load_config
import pysolr
import math

config = load_config()

app = Flask(__name__)

solr_host = config['solr_host']
solr_port = config['solr_port']
solr_core = config['solr_core']

solr_url = f"http://{solr_host}:{solr_port}/solr/{solr_core}"

solr = pysolr.Solr(solr_url)

import requests

def spellcheck(query):
    params = {
        'q': query,
        'spellcheck': 'true',
        'spellcheck.count': 5,
        'wt': 'json'
    }
    response = requests.get(f'http://localhost:{solr_port}/solr/{solr_core}/spell', params=params)
    data = response.json()
    suggestions_raw  = data.get('spellcheck', {}).get('suggestions', [])

    results = []
    i = 0
    while i < len(suggestions_raw):
        if isinstance(suggestions_raw[i], str):
            details = suggestions_raw[i + 1]
            for s in details.get("suggestion", []):
                word = s.get("word")
                freq = s.get("freq")
                results.append((word, freq))
            i += 2
        else:
            i += 1
    return results


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    suggested = request.args.get("suggested", "").lower() == "true"
    page = int(request.args.get("page", 1))
    results = []
    solr_filters = []
    total_pages = 1
    num_of_hits = 0

    if not query:
        query = "*:*"

    if query:
        for key, value in request.args.items():
            if key.startswith("filter_"):
                field = key[7:]
                solr_filters.append(f"{field}:\"{value}\"")

        params = {
            "qf": "title^5 author_names^3 summary^2 fulltext concepts spellcheck_base^1",
            "defType": "edismax",         
            "fl": "*,score",
            "fq": solr_filters,
            "debugQuery": "true",
            "bf": "log(cited_by_count)^2",
            "start": (page - 1) * 10,
            "rows": 10,
            "facet": "true",
            "facet.field": ["concepts", "open_access", "language", "journal", "type"],
            "facet.limit": 10,
            "facet.mincount": 1
            }

        solr_results = solr.search(query, **params)
        results = solr_results.docs
        num_of_hits = solr_results.hits
        total_pages = max(1, math.ceil(num_of_hits / 10))
        facets = solr_results.facets.get("facet_fields", {}) if hasattr(solr_results, 'facets') else {}

        spell_suggestions = []
        if not suggested:
            raw_suggestions = spellcheck(query)
            spell_suggestions = [(w, f) for w, f in raw_suggestions if w.lower() != query.lower()]

    return render_template("index.html", 
                           query=query, 
                           results=results, 
                           num_of_hits=num_of_hits, 
                           page=page, 
                           total_pages=total_pages,
                           suggestions=spell_suggestions,
                           facets=facets)

if __name__ == "__main__":
    app.run(debug=True)