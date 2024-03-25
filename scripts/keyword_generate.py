import os
import json
import yake
import uuid
import csv
from thefuzz import fuzz
from typing import Dict, List

extractor = yake.KeywordExtractor()


def update_keywords(all_keywords: Dict[str, List[str]], new_keyword: str, paper: Dict[str, str]) -> None:
    merged_with = []
    current_keywords = list(all_keywords.keys())

    for keyword in current_keywords:
        if fuzz.token_sort_ratio(keyword, new_keyword) > 75:
            current_paper_ids = all_keywords.get(keyword, [])
            current_paper_ids.append(paper['paperId'])
            all_keywords.pop(keyword, None)
            new_keyword = new_keyword if len(
                new_keyword) < len(keyword) else keyword

            all_keywords[new_keyword] = current_paper_ids
            merged_with.append(keyword)

    if len(merged_with) == 0:
        all_keywords[new_keyword] = [paper['paperId']]
        # print(f'Merged {new_keyword} with {','.join(merged_with)}')


with open('./csv/keywords.csv', 'w', encoding="utf-8") as output_nodes, open('./csv/keywords_papers.csv', 'w', encoding="utf-8") as output_relationships:
    # keyword -> [paper_id]
    all_keywords: Dict[str, List[str]] = {}

    nodes_writer = csv.writer(output_nodes, quoting=csv.QUOTE_STRINGS)
    relationships_writer = csv.writer(
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
                    update_keywords(all_keywords, value, paper)

    for (keyword, paper_ids) in all_keywords.items():
        keyword_id = str(uuid.uuid4())

        for paper_id in paper_ids:
            relationships_writer.writerow([
                keyword_id,
                paper_id,
            ])

        nodes_writer.writerow([
            keyword_id,
            str(keyword).lower(),
        ])
