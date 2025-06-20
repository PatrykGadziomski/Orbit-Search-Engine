"""
Author: Patryk Gadziomski
Updated: 19.06.2025
"""

import urllib
import xml.etree.ElementTree as ET
import json
from typing import Dict
import requests
import fitz
import io
import time
from tqdm import tqdm


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
        try:
            response = requests.get(pdf_url)
            pdf_bytes = io.BytesIO(response.content)
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            return text
        except:
            return ""
    else:
        return ""


def access_arxiv_data(max_results: int, max_total: int, file_path: str) -> None:
    for start in range(0, max_total, max_results):

        query = '((ti:"artificial intelligence" OR ti:"machine learning" OR ti:"deep learning" OR ti:"computer vision" OR ti:"natural language processing" OR ti:"robotics" OR ti:"autonomous systems" OR ti:"automation") OR (abs:"artificial intelligence" OR abs:"machine learning" OR abs:"deep learning" OR abs:"computer vision" OR abs:"natural language processing" OR abs:"robotics" OR abs:"autonomous systems" OR abs:"automation")) AND ((ti:satellite OR ti:spacecraft OR ti:aerospace OR ti:"remote sensing" OR ti:"earth observation" OR ti:"space exploration" OR ti:"planetary science") OR (abs:satellite OR abs:spacecraft OR abs:aerospace OR abs:"remote sensing" OR abs:"earth observation" OR abs:"space exploration" OR abs:"planetary science"))'
        encoded_query = urllib.parse.quote(query)

        url = f'http://export.arxiv.org/api/query?search_query={encoded_query}&sortBy=lastUpdatedDate&sortOrder=ascending&start={start}&max_results={max_results}'
        response = urllib.request.urlopen(url)
        xml_data = response.read().decode('utf-8')

        root = ET.fromstring(xml_data)

        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id')
            doi_elem = entry.find('{http://arxiv.org/schemas/atom}doi')
            title = entry.find('{http://www.w3.org/2005/Atom}title')
            summary = entry.find('{http://www.w3.org/2005/Atom}summary')
            publication_date = entry.find('{http://www.w3.org/2005/Atom}published')
            update_year = entry.find('{http://www.w3.org/2005/Atom}updated')
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
            paper_link = entry.find('{http://www.w3.org/2005/Atom}id')
            journal_ref = entry.find('{http://arxiv.org/schemas/atom}journal_ref')
            categories = [c.attrib['term'] for c in entry.findall('{http://www.w3.org/2005/Atom}category')]
            pdf_link = next((link.attrib['href'] for link in entry.findall('{http://www.w3.org/2005/Atom}link') if link.attrib.get('title') == 'pdf'), None)
            full_text = parse_text_from_pdf(pdf_url=pdf_link)

            arxiv_id = arxiv_id.text.strip() if arxiv_id is not None else None
            doi = doi_elem.text if doi_elem is not None else None
            title = title.text.strip() if title is not None else None
            summary = summary.text.strip() if summary is not None else None
            publication_date = publication_date.text if publication_date is not None else None
            update_year = update_year.text if update_year is not None else None
            authors = authors if authors is not None else None
            paper_link = paper_link.text if paper_link is not None else None
            journal_ref = journal_ref.text if journal_ref is not None else None
            categories = categories if categories is not None else None
            pdf_link = pdf_link if pdf_link is not None else None
            full_text = full_text if full_text is not None else None

            paper = {
                'arxiv_id': arxiv_id,
                'doi': doi,
                'title': title,
                'summary': summary,
                'published': publication_date,
                'updated': update_year,
                'authors': authors,
                'link': paper_link,
                'journal': journal_ref,
                'category': categories,
                'pdf_link': pdf_link,
                'full_text': full_text
            }

            append_to_jsonl(file_path=file_path, record=paper)
            print('- ', arxiv_id, 'paper added.')
            time.sleep(2)


def enrich_paper(paper, match):
    return {
        'arxiv_id': paper.get('arxiv_id'),
        'doi': paper.get('doi'),
        'title': paper.get('title'),
        'summary': paper.get('summary'),
        'published': paper.get('published'),
        'updated': paper.get('updated'),
        'authors': paper.get('authors'),
        'link': paper.get('link'),
        'journal': paper.get('journal'),
        'category': paper.get('category'),
        'pdf_link': paper.get('pdf_link'),
        'full_text': paper.get('full_text'),

        # OpenAlex-Data
        'openalex_id': match.get('id'),
        'concepts': match.get('concepts'),
        'cited_by_count': match.get('cited_by_count'),
        'host_venue': match.get('host_venue', {}).get('display_name'),
        'open_access': match.get('open_access', {}).get('is_oa'),

        # Enriched Data
        'type': match.get('type'),
        'language': match.get('language'),
        'host_venue_license': match.get('host_venue', {}).get('license'),
        'is_paratext': match.get('is_paratext'),
        'authorships': match.get('authorships'),
        'referenced_works': match.get('referenced_works'),
        'related_works': match.get('related_works'),
        'biblio': match.get('biblio'),
        'institutions': match.get('institutions'),
        'grants': match.get('grants'),
        'primary_location': match.get('primary_location'),
        'mesh': match.get('mesh'),
        'keywords': match.get('keywords')
    }


def fetch_openalex_data(url, params=None):
    try:
        response = requests.get(url=url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Kein Ergebnis von OpenAlex (Status {response.status_code}) für URL: {url}")
    except Exception as e:
        print(f"Fehler beim Zugriff auf OpenAlex: {e}")
    return None


def access_openalex_data(data, file_path):
    for paper in tqdm(data):
        match = None

        # 1. Search via DOI
        if paper.get('doi'):
            encoded_doi = urllib.parse.quote(f"https://doi.org/{paper['doi']}")
            url = f"https://api.openalex.org/works/{encoded_doi}"
            match = fetch_openalex_data(url)

        # 2. Search via ArXiv-ID
        if not match and paper.get('arxiv_id'):
            arxiv_id = urllib.parse.quote(paper['arxiv_id'].replace("http://arxiv.org/abs/", ""))
            url = f"https://api.openalex.org/works/arxiv:{arxiv_id}"
            match = fetch_openalex_data(url)

        # 3. Search via Title
        if not match and paper.get('title'):
            url = 'https://api.openalex.org/works'
            params = {'filter': f'title.search:"{paper["title"]}"'}
            result = fetch_openalex_data(url, params)
            if result and result.get('results'):
                match = result['results'][0]

        # Save results, if existing
        if match:
            enriched = enrich_paper(paper, match)
            append_to_jsonl(file_path=file_path, record=enriched)
        else:
            print(f"Keine passenden OpenAlex-Daten für Paper: {paper.get('title', 'Unbekannt')}")


def main_access(arxiv_file_path, eriched_file_path):
    print('Start accessing ArXiv Data.')
    access_arxiv_data(300, 20000, arxiv_file_path) # Change numbers for more/less data
    data = read_jsonl(arxiv_file_path)
    print('Start accessing OpenAlex Data.') 
    access_openalex_data(data=data, file_path=eriched_file_path)