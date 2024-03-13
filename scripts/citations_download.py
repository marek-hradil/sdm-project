import os
import json
from pathlib import Path
import requests
from typing import List
import time


BASE_URL = 'https://api.semanticscholar.org/graph/v1'
PAPERS_URL = f'{BASE_URL}/paper/search/bulk?fields=paperId,title,publicationVenue,year,authors,abstract,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,citationCount&sort=citationCount:desc&fieldsOfStudy=Computer Science,Mathematics'
CITATIONS_URL = f'{BASE_URL}/paper/batch?fields=paperId,citations'


REQUEST_TIMEOUT = 10000


def get_url():
    return CITATIONS_URL


def download(paperIds: List[str], filename: str, index: int):
    print(f'Requesting papers for {filename}')
    request = requests.post(url=get_url(), json={
        "ids": paperIds}, timeout=REQUEST_TIMEOUT)
    data = request.json()

    if "message" in data:
        print("Retrying")
        time.sleep(1)
        return download(paperIds, filename, index)

    with open(f'./json/citations/{filename}_part_{index}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


for file in os.listdir('./json/papers'):
    with open(f'./json/papers/{file}', 'r', encoding='utf-8') as f:
        data = json.load(f)
        paperIds = [paper['paperId'] for paper in data]
        chunks = [paperIds[x:x+500] for x in range(0, len(paperIds), 500)]
        filename = Path(file).stem

        for index, chunk in enumerate(chunks):
            download(chunk, filename, index)
