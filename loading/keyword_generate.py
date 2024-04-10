import os
import json
import yake
import uuid
import csv
from thefuzz import fuzz
from typing import Dict, List

extractor = yake.KeywordExtractor()


def append_keywords(all_keywords: Dict[str, List[str]], new_keyword: str, paper: Dict[str, str]) -> None:
    merged_with = []
    current_keywords = list(all_keywords.keys())

    for keyword in current_keywords:
        if fuzz.token_sort_ratio(keyword, new_keyword) <= 75:
            continue

        current_paper_ids = all_keywords.get(keyword, [])
        current_paper_ids.append(paper['paperId'])
        all_keywords.pop(keyword, None)
        new_keyword = new_keyword if len(
            new_keyword) < len(keyword) else keyword

        all_keywords[new_keyword] = current_paper_ids
        merged_with.append(keyword)

    if len(merged_with) == 0:
        all_keywords[new_keyword] = [paper['paperId']]


def replace_top_7_keywords(all_keywords: Dict[str, List[str]]):
    top_keywords = sorted(all_keywords, reverse=True,
                          key=lambda x: len(all_keywords[x]))[:7]
    existing_keywords = list(all_keywords.keys())

    if 'data management' not in existing_keywords:
        all_keywords['data management'] = all_keywords[top_keywords[0]]

    if 'indexing' not in existing_keywords:
        all_keywords['indexing'] = all_keywords[top_keywords[1]]

    if 'data modeling' not in existing_keywords:
        all_keywords['data modeling'] = all_keywords[top_keywords[2]]

    if 'data processing' not in existing_keywords:
        all_keywords['data processing'] = all_keywords[top_keywords[3]]

    if 'data storage' not in existing_keywords:
        all_keywords['data storage'] = all_keywords[top_keywords[4]]

    if 'data querying' not in existing_keywords:
        all_keywords['data querying'] = all_keywords[top_keywords[5]]

    if 'big data' not in existing_keywords:
        all_keywords['big data'] = all_keywords[top_keywords[6]]


def write_keyword(keyword, paper_ids, relationship_writer, nodes_writer):
    keyword_id = str(uuid.uuid4())

    for paper_id in paper_ids:
        relationship_writer.writerow([
            keyword_id,
            paper_id,
        ])

    nodes_writer.writerow([
        keyword_id,
        str(keyword).lower(),
    ])


def run_stage():
    with open('./csv/keywords.csv', 'w', encoding="utf-8") as output_nodes, open('./csv/keywords_papers.csv', 'w', encoding="utf-8") as output_relationships:
        # keyword -> [paper_id]
        all_keywords: Dict[str, List[str]] = {}

        keywords_nodes_writer = csv.writer(
            output_nodes, quoting=csv.QUOTE_STRINGS)
        keywords_relationships_writer = csv.writer(
            output_relationships, quoting=csv.QUOTE_STRINGS)

        for file in os.listdir('./json/papers'):
            with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
                data = json.load(input)

                for index, paper in enumerate(data):
                    abstract = (paper['abstract'] or '')
                    if not abstract:
                        continue

                    print(f'{index}/{len(data)} in {file[0:20]}')

                    keywords = extractor.extract_keywords(abstract)
                    for (value, _) in keywords[:5]:
                        append_keywords(all_keywords, value, paper)

        replace_top_7_keywords(all_keywords)

        for (keyword, paper_ids) in all_keywords.items():
            write_keyword(keyword, paper_ids,
                          keywords_relationships_writer, keywords_nodes_writer)


if __name__ == '__main__':
    run_stage()
