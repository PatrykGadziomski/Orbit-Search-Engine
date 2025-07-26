from flask import Flask, request, render_template, jsonify
from orbit_utils.orbit_config_loader import load_config
import pysolr
import math
import requests

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


@app.route('/mlt', methods=['POST'])
def get_mlt():
    try:
        doc_id = request.json.get('doc_id')
        if not doc_id:
            return jsonify({'error': 'No doc_id provided', 'docs': []})
            
        print(f"MLT Request für doc_id: {doc_id}")  # Debug-Output
        
        # Teste zunächst, ob das Dokument überhaupt existiert
        test_queries = [
            f'openalex_id:"{doc_id}"',
            f'arxiv_id:"{doc_id}"', 
            f'doi:"{doc_id}"',
            f'id:"{doc_id}"'
        ]
        
        found_doc = None
        working_query = None
        
        # Erst prüfen, ob Dokument existiert
        for test_query in test_queries:
            test_params = {
                'q': test_query,
                'rows': 1,
                'wt': 'json'
            }
            test_resp = requests.get(f'http://localhost:{solr_port}/solr/{solr_core}/select', params=test_params)
            print(f"Test Query: {test_query}, Status: {test_resp.status_code}")
            
            if test_resp.status_code == 200:
                test_data = test_resp.json()
                if test_data.get('response', {}).get('numFound', 0) > 0:
                    found_doc = test_data['response']['docs'][0]
                    working_query = test_query
                    print(f"Documents with Query: {test_query}")
                    break
        
        if not found_doc:
            print(f"Document with ID {doc_id} not found")
            return jsonify({'error': 'Document not found', 'docs': []})
        
        # Jetzt MLT versuchen
        mlt_params = {
            'q': working_query,
            'mlt': 'true',
            'mlt.fl': 'title,summary,concepts',  # Vereinfachte Felder
            'mlt.mindf': 1,
            'mlt.mintf': 1,
            'mlt.count': 5,
            'fl': 'title,summary,openalex_id,arxiv_id,doi,authorships_names,published,cited_by_count,score',
            'wt': 'json'
        }
        
        mlt_resp = requests.get(f'http://localhost:{solr_port}/solr/{solr_core}/mlt', params=mlt_params)
        print(f"MLT Response Status: {mlt_resp.status_code}")
        
        if mlt_resp.status_code == 200:
            mlt_data = mlt_resp.json()
            print(f"MLT Response: {mlt_data}")
            similar_docs = mlt_data.get('response', {}).get('docs', [])
            return jsonify(similar_docs)
        else:
            print(f"MLT Error: {mlt_resp.status_code}, {mlt_resp.text}")
            return jsonify({'error': f'MLT request failed: {mlt_resp.status_code}', 'docs': []})
        
    except Exception as e:
        print(f"MLT Exception: {str(e)}")
        app.logger.error(f"MLT Error for doc_id {doc_id}: {str(e)}")
        return jsonify({'error': str(e), 'docs': []})


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