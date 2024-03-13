import os
import json

with open('./csv/papers.csv', 'w', encoding="utf-8") as output:
    for file in os.listdir('./json/papers'):
        with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                paper_id = paper['paperId']
                title = paper['title']
                abstract = (paper['abstract'] or '').replace(
                    '\n', ' ').replace('\r', ' ')
                year = str(paper['year'])
                citation_count = paper['citationCount']

                row = [
                    paper_id,
                    title,
                    abstract,
                    str(year),
                    str(citation_count)
                ]

                output.write(
                    ','.join(row) + '\n'
                )
