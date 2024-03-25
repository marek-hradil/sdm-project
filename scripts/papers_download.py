import requests
import time
from typing import List, Optional
import json
from uuid import uuid4
from datetime import datetime

BASE_URL = 'https://api.semanticscholar.org/graph/v1'
PAPERS_FIELDS = 'paperId,title,publicationVenue,year,authors,abstract,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,citationCount,citations'
PAPERS_URL = f'{BASE_URL}/paper/batch?fields={PAPERS_FIELDS}'
DEPTH_LIMIT = 2
REQUEST_TIMEOUT = 10000
FILE_ENTITIES_LIMIT = 5000


def download(ids: List[str]):
    print(f'[{datetime.now()}] Requesting papers for {ids[:10]}')
    params = {"ids": ids}
    request = requests.post(url=PAPERS_URL,
                            json=params,
                            timeout=REQUEST_TIMEOUT)
    data = request.json()

    if 'message' in data:
        print('Retrying')
        time.sleep(1)
        return download(ids)

    if 'error' in data:
        print(f'Error: {data['error']}')
        return None

    print(f'[{datetime.now()}] Retrieved {len(data)} papers')

    return [paper for paper in data if paper is not None and paper['paperId'] is not None]


def flatten(data):
    return [item for sublist in data for item in sublist]


def save_papers(papers: List[dict]):
    with open(f'./json/papers/{uuid4()}.json', 'w', encoding="utf-8") as output:
        json.dump(papers, output)

    print(f'[{datetime.now()}] Saved {len(papers)} papers')
    papers.clear()


def save_citations(citations: List[tuple]):
    with open(f'./json/citations/{uuid4()}.json', 'w', encoding="utf-8") as output:
        json.dump(citations, output)

    print(f'[{datetime.now()}] Saved {len(citations)} citations')
    citations.clear()


def traverse(ids: List[str], depth: int, downloaded_papers: List[dict], downloaded_citations: List[tuple], parent_id: Optional[str] = None):
    if depth > DEPTH_LIMIT:
        return

    print(f'[{datetime.now()}] Entering for parent {
          parent_id} with depth {depth} fetching {len(ids)} papers')

    chunks = [ids[i:i + 500] for i in range(0, len(ids), 500)]
    papers = flatten(
        [download(chunk) for chunk in chunks])
    downloaded_papers.extend(papers)

    if parent_id is not None:
        citations = [(parent_id, paper['paperId'])
                     for paper in papers]

        downloaded_citations.extend(citations)

    if len(downloaded_papers) > FILE_ENTITIES_LIMIT:
        save_papers(downloaded_papers)
    else:
        print(f'[{datetime.now()}] Capacity of papers: {
              len(downloaded_papers)}/{FILE_ENTITIES_LIMIT}')

    if len(downloaded_citations) > FILE_ENTITIES_LIMIT:
        save_citations(downloaded_citations)
    else:
        print(f'[{datetime.now()}] Capacity of citations: {
              len(downloaded_citations)}/{FILE_ENTITIES_LIMIT}')

    for paper in papers:
        print(f'[{datetime.now()}] Descending to {
              paper["paperId"]} with {len(paper['citations'])} citations')
        traverse([citation['paperId']
                 for citation in paper['citations']], depth=depth + 1, downloaded_papers=downloaded_papers, downloaded_citations=downloaded_citations, parent_id=paper['paperId'])


downloaded_papers = []
downloaded_citations = []

# Robust and Adaptive Control - Most cited 2024
ROOT_ID = '78d4d60c50b23182f38df267d595a3b467db1250'

traverse([ROOT_ID], depth=0, downloaded_papers=downloaded_papers,
         downloaded_citations=downloaded_citations)

if len(downloaded_papers) > 0:
    save_papers(downloaded_papers)

if len(downloaded_citations) > 0:
    save_citations(downloaded_citations)
