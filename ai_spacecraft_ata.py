import urllib, urllib.request
import xml.etree.ElementTree as ET
import json

results = []
index_id = 0

for start in range(0, 2000, 10):
    query = '("artificial intelligence" OR "machine learning" OR "deep learning" OR "ai" OR "computer vision") AND ("satellite" OR "orbital" OR "spacecraft" OR "earth observation" OR "remote sensing" OR "aerospace" OR "planetary" OR "space exploration" OR "astroinformatics" OR "telemetry" OR "space mission" OR "mission control" OR "earth observation satellite" OR "hyperspectral imaging" OR "satellite communication" OR "AI for earth observation" OR "autonomous navigation" OR "remote sensing data" OR "predictive maintenance")'
    encoded_query = urllib.parse.quote(query)

    url = f'http://export.arxiv.org/api/query?search_query={encoded_query}&sortBy=lastUpdatedDate&sortOrder=ascending&start={start}&max_results=10'
    response = urllib.request.urlopen(url)
    xml_data = response.read().decode('utf-8')
    
    root = ET.fromstring(xml_data)

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper = {
            'api_id': index_id,
            'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
            'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
            'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
            'updated': entry.find('{http://www.w3.org/2005/Atom}updated').text,
            'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
            'link': entry.find('{http://www.w3.org/2005/Atom}id').text,
            'pdf_link': next((link.attrib['href'] for link in entry.findall('{http://www.w3.org/2005/Atom}link') if link.attrib.get('title') == 'pdf'), None)

        }
        results.append(paper)
        index_id += 1
        print(index_id, 'Paper was added to list!')

with open('arxiv_papers_ki_raumfahrt.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"{len(results)} Paper gespeichert.")