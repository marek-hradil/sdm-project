import os
import json
import csv


def remove_lineends(s):
    return (s or '').replace('\n', ' ').replace('\r', ' ')


with open('./csv/papers.csv', 'w', encoding="utf-8") as output:
    writer = csv.writer(output)

    for file in os.listdir('./json/papers'):
        with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                paper_id = paper['paperId']
                title = remove_lineends(paper['title'])
                abstract = remove_lineends(paper['abstract'])
                year = paper['year']
                citation_count = paper['citationCount']

                writer.writerow([
                    paper_id,
                    title,
                    abstract,
                    year,
                    citation_count
                ])
