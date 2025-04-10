import urllib, urllib.request
import xml.etree.ElementTree as ET
import json

results = []

for start in range(0, 30, 10):
    query = '("artificial intelligence" OR "machine learning" OR "deep learning") AND (space OR satellite OR orbital)'
    encoded_query = urllib.parse.quote(query)

    url = f'http://export.arxiv.org/api/query?search_query={encoded_query}&sortBy=lastUpdatedDate&sortOrder=ascending&start={start}&max_results=10'
    response = urllib.request.urlopen(url)
    xml_data = response.read().decode('utf-8')

    
    root = ET.fromstring(xml_data)

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper = {
            'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
            'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
            'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
            'updated': entry.find('{http://www.w3.org/2005/Atom}updated').text,
            'authors': [author.find('{http://www.w3.org/2005/Atom}name').text
                        for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
            'link': entry.find('{http://www.w3.org/2005/Atom}id').text
        }
        results.append(paper)

# Als JSON speichern
with open('arxiv_papers_ki_raumfahrt.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"{len(results)} Paper gespeichert.")