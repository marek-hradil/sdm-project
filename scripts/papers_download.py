import requests
import time
from typing import Optional
import json

BASE_URL = 'https://api.semanticscholar.org/graph/v1'
PAPERS_URL = f'{BASE_URL}/paper/search/bulk?fields=paperId,title,publicationVenue,year,authors,abstract,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,citationCount&sort=citationCount:desc&fieldsOfStudy=Computer Science,Mathematics'
CITATIONS_URL = f'{BASE_URL}/paper/batch?fields=paperId,citations'

REQUEST_TIMEOUT = 10000
MIN_CITATION_LIMIT = 100
YEARS_TO_FETCH = [2020, 2021, 2022, 2023, 2024]
CITATION_REQUEST_LIMIT = 500


def get_url(token: str, year: int):
    url = f'{PAPERS_URL}&year={year}&minCitationCount={MIN_CITATION_LIMIT}'
    if token:
        url += f'&token={token}'

    return url


def download(year: int, token: Optional[str] = None):
    print(f'Requesting papers for {year}, token {token}')
    request = requests.get(url=get_url(token, year),
                           timeout=REQUEST_TIMEOUT)
    data = request.json()

    if 'data' not in data:
        time.sleep(1)
        return download(year, token)

    with open(f'./json/papers/{year}_{token}_{MIN_CITATION_LIMIT}.json', 'w', encoding='utf-8') as f:
        json.dump(data['data'], f)

    if data['token']:
        print('Continuing in the same year')
        download(year, token=data['token'])


for year in YEARS_TO_FETCH:
    download(year)
