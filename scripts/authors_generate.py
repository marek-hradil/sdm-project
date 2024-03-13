import os
import json

with open('./csv/authors.csv', 'w', encoding="utf-8") as output_nodes, open('./csv/authors_papers.csv', 'w', encoding="utf-8") as output_relationships:
    for file in os.listdir('./json/papers'):
        with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                authors = paper['authors'] or []

                for author in authors:
                    author_id = author['authorId']
                    name = author['name']

                    if not author_id or not name:
                        continue

                    row = [
                        author_id,
                        name
                    ]

                    output_nodes.write(
                        ','.join(row) + '\n'
                    )

                    output_relationships.write(
                        f"{author_id},{paper['paperId']}\n"
                    )
