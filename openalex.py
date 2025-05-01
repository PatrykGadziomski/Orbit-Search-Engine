import json
import requests
import time

# Lade arXiv-Paper
with open('arxiv_papers_ki_raumfahrt.json', 'r', encoding='utf-8') as f:
    arxiv_papers = json.load(f)

openalex_results = []

for paper in arxiv_papers[:1]:  # zum Testen erstmal nur eins
    doi = paper.get('doi')
    enriched = None

    if doi:
        doi_encoded = requests.utils.quote(doi)
        url = f"https://api.openalex.org/works/doi:{doi_encoded}"
        print(f"🔍 Suche OpenAlex für DOI: {doi}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                match = response.json()
                enriched = {
                    'arxiv_title': paper['title'],
                    'arxiv_authors': paper['authors'],
                    'openalex_id': match.get('id'),
                    'doi': match.get('doi'),
                    'concepts': match.get('concepts'),
                    'cited_by_count': match.get('cited_by_count'),
                    'publication_year': match.get('publication_year'),
                    'host_venue': match.get('host_venue', {}).get('display_name'),
                    'open_access': match.get('open_access', {}).get('is_oa'),
                    'original_openalex': match
                }
            else:
                print(f"❌ Kein Ergebnis für DOI: {doi} (Status {response.status_code})")
        except Exception as e:
            print(f"💥 Fehler bei DOI {doi}: {e}")

    if not enriched:
        # Wenn DOI nicht ging oder nicht vorhanden → fallback auf Titel
        title = paper['title']
        print(f"🔍 Fallback: Suche mit Titel in OpenAlex: {title}")
        response = requests.get(
            'https://api.openalex.org/works',
            params={'filter': f'title.search:"{title}"'},
            timeout=10
        )
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            match = data['results'][0]
            enriched = {
                'arxiv_title': title,
                'arxiv_authors': paper['authors'],
                'openalex_id': match.get('id'),
                'doi': match.get('doi'),
                'concepts': match.get('concepts'),
                'cited_by_count': match.get('cited_by_count'),
                'publication_year': match.get('publication_year'),
                'host_venue': match.get('host_venue', {}).get('display_name'),
                'open_access': match.get('open_access', {}).get('is_oa'),
                'original_openalex': match
            }
        else:
            print("⚠️ Kein Treffer per Titel")

    if enriched:
        openalex_results.append(enriched)

    time.sleep(1)

# Speichern
with open('arxiv_with_openalex.json', 'w', encoding='utf-8') as f:
    json.dump(openalex_results, f, indent=2, ensure_ascii=False)

print(f"\n✅ {len(openalex_results)} Paper mit OpenAlex-Daten angereichert.")
