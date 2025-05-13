import urllib
import xml.etree.ElementTree as ET
import json
from typing import Dict
import requests
import fitz
import io

def read_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(row) for row in f]


def append_to_jsonl(file_path: str, record: Dict) -> None:
    try:
        with open(file_path, mode='a', encoding='utf-8') as f:
            json.dump(record, f)
            f.write('\n')
    except IOError as e:
        raise IOError(f"Failed to write to file {file_path}: {e}")


def parse_text_from_pdf(pdf_url):
    if pdf_url:
        response = requests.get(pdf_url)
        pdf_bytes = io.BytesIO(response.content)  # Lade in speicherbasiertes File-Objekt
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        return text


def access_arxiv_data(start_: int, end_: int) -> None:
    for start in range(0, start_, end_):
        query = 'all:("artificial intelligence" OR "machine learning" OR "deep learning" OR "ai" OR "computer vision" OR "natural language processing" OR "nlp" OR "robotics" OR "automation") AND all:("satellite" OR "orbital" OR "spacecraft" OR "earth observation" OR "remote sensing" OR "aerospace" OR "planetary" OR "space exploration" OR "astroinformatics" OR "telemetry" OR "space mission" OR "mission control" OR "earth observation satellite" OR "hyperspectral imaging" OR "satellite communication" OR "AI for earth observation" OR "autonomous navigation" OR "remote sensing data" OR "predictive maintenance")'
        encoded_query = urllib.parse.quote(query)

        url = f'http://export.arxiv.org/api/query?search_query={encoded_query}&sortBy=lastUpdatedDate&sortOrder=ascending&start={start}&max_results=10'
        response = urllib.request.urlopen(url)
        xml_data = response.read().decode('utf-8')

        root = ET.fromstring(xml_data)

        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            doi_elem = entry.find('{http://arxiv.org/schemas/atom}doi')
            doi = doi_elem.text if doi_elem is not None else None

            journal_ref_elem = entry.find('{http://arxiv.org/schemas/atom}journal_ref')
            journal_ref = journal_ref_elem.text if journal_ref_elem is not None else None

            arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
            pdf_link = next((link.attrib['href'] for link in entry.findall('{http://www.w3.org/2005/Atom}link') if link.attrib.get('title') == 'pdf'), None)

            paper = {
                'arxiv_id': arxiv_id,
                'doi': doi,
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'updated': entry.find('{http://www.w3.org/2005/Atom}updated').text,
                'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'link': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'journal': journal_ref,
                'category': [c.attrib['term'] for c in entry.findall('{http://www.w3.org/2005/Atom}category')],
                'pdf_link': pdf_link,
                'full_text': parse_text_from_pdf(pdf_url=pdf_link)
            }

            append_to_jsonl(file_path=r'data_accessing/arxiv_papers_int_aerospace.jsonl', record=paper)


def access_openalex_data(data):
    # Suche: DOI; ArXiv.ID, Title
    for paper in data:
        doi = True if paper['doi'] != None else False
        arxiv_id = True if paper['arxiv_id'] != None else False
        title = True if paper['title'] != None else False

        if doi:
            encoded_doi = urllib.parse.quote(f"https://doi.org/{paper['doi']}")
            url = f"https://api.openalex.org/works/{encoded_doi}"

            try:
                response = requests.get(url=url, timeout=10)
                if response.status_code == 200:
                    match = response.json()

                    paper = {
                        'arxiv_id': paper['arxiv_id'],
                        'doi': paper['doi'],
                        'title': paper['title'],
                        'summary': paper['summary'],
                        'published': paper['published'],
                        'updated': paper['updated'],
                        'authors': paper['authors'],
                        'link': paper['link'],
                        'journal': paper['journal'],
                        'category': paper['category'],
                        'pdf_link': paper['pdf_link'],
                        'full_text': paper['full_text'],
                        'openalex_id': match.get('id'),
                        'concepts': match.get('concepts'),
                        'cited_by_count': match.get('cited_by_count'),
                        'host_venue': match.get('host_venue', {}).get('display_name'),
                        'open_access': match.get('open_access', {}).get('is_oa')
                        # TODO: Add more data
                    }
                    append_to_jsonl(file_path=r'data_accessing/arxivANDopenalex_papers_int_aerospace.jsonl', record=paper)
                else:
                    print(f"Kein Ergebnis für DOI: {paper['doi']} (Status {response.status_code})")
            except Exception as e:
                    print(f"Fehler bei DOI {paper['doi']}: {e}")

        elif arxiv_id: # FIX: 'module' is not callable
            encoded_arxiv_id = urllib.parse.quote(paper['arxiv_id'])
            url = f"https://api.openalex.org/works/arxiv:{encoded_arxiv_id}"
            try:
                response = requests(url=url, timeout=10)
                if response.status_code == 200:
                    match = response.json()

                    paper = {
                        'arxiv_id': paper['arxiv_id'],
                        'doi': paper['doi'],
                        'title': paper['title'],
                        'summary': paper['summary'],
                        'published': paper['published'],
                        'updated': paper['updated'],
                        'authors': paper['authors'],
                        'link': paper['link'],
                        'journal': paper['journal'],
                        'category': paper['category'],
                        'pdf_link': paper['pdf_link'],
                        'full_text': paper['full_text'],
                        'openalex_id': match.get('id'),
                        'concepts': match.get('concepts'),
                        'cited_by_count': match.get('cited_by_count'),
                        'host_venue': match.get('host_venue', {}).get('display_name'),
                        'open_access': match.get('open_access', {}).get('is_oa')
                        # TODO: Add more data
                    }
                    append_to_jsonl(file_path=r'data_accessing/arxivANDopenalex_papers_int_aerospace.jsonl', record=paper)
                else:
                    print(f"Kein Ergebnis für ArXiv ID: {paper['arxiv_id']} (Status {response.status_code})")
            except Exception as e:
                    print(f"Fehler bei ArXiv ID {paper['arxiv_id']}: {e}")

        elif title:
            url = 'https://api.openalex.org/works'
            params = {'filter': f'title.search:"{paper["title"]}"'}

            try:
                response = requests.get(url=url, params=params, timeout=10)
                if response.status_code == 200:
                    match = response.json()

                    paper = {
                        'arxiv_id': paper['arxiv_id'],
                        'doi': paper['doi'],
                        'title': paper['title'],
                        'summary': paper['summary'],
                        'published': paper['published'],
                        'updated': paper['updated'],
                        'authors': paper['authors'],
                        'link': paper['link'],
                        'journal': paper['journal'],
                        'category': paper['category'],
                        'pdf_link': paper['pdf_link'],
                        'full_text': paper['full_text'],
                        'openalex_id': match.get('id'),
                        'concepts': match.get('concepts'),
                        'cited_by_count': match.get('cited_by_count'),
                        'host_venue': match.get('host_venue', {}).get('display_name'),
                        'open_access': match.get('open_access', {}).get('is_oa')
                        # TODO: Add more data
                    }
                    append_to_jsonl(file_path=r'data_accessing/arxivANDopenalex_papers_int_aerospace.jsonl', record=paper)
                else:
                    print(f"Kein Ergebnis für Titel: {paper['title']} (Status {response.status_code})")
            except Exception as e:
                    print(f"Fehler bei Titel {paper['title']}: {e}")

        else:
            print('Paper could not be enriched.')


if __name__ == "__main__":
    print('Start accessing ArXiv Data.')
    access_arxiv_data(10, 10)
    data = read_jsonl(r'data_accessing/arxiv_papers_int_aerospace.jsonl')
    print('Start accessing OpenAlex Data.') 
    access_openalex_data(data=data)
