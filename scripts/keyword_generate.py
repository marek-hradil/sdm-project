import os
import json
import yake
import uuid

extractor = yake.KeywordExtractor()

with open('./csv/keywords.csv', 'w', encoding="utf-8") as output_nodes, open('./csv/keywords_papers.csv', 'w', encoding="utf-8") as output_relationships:
    for file in os.listdir('./json/papers'):
        with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                abstract = (paper['abstract'] or '')
                if not abstract:
                    continue

                keywords = extractor.extract_keywords(abstract)
                for keyword in keywords:
                    keyword_id = str(uuid.uuid4())

                    output_nodes.write(
                        f"{keyword_id},{keyword}\n"
                    )

                    output_relationships.write(
                        f"{keyword_id},{paper['paperId']}\n"
                    )
