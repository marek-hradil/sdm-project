import os
import json
import csv


def remove_lineends(s):
    return (s or '').replace('\n', ' ').replace('\r', ' ')


with open('./csv/papers.csv', 'w', encoding="utf-8") as output:
    writer = csv.writer(output, quoting=csv.QUOTE_STRINGS)

    for file in os.listdir('./json/papers'):
        with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                if paper['year'] is None:
                    continue

                paper_id = paper['paperId']
                title = remove_lineends(paper['title'])
                abstract = remove_lineends(paper['abstract'])
                year = int(paper['year'])
                citation_count = int(paper['citationCount'] or 0)

                writer.writerow([
                    paper_id,
                    title,
                    abstract,
                    year,
                    citation_count
                ])
