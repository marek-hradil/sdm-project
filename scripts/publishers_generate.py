import os
import json
import csv

with open('./csv/publishers.csv', 'w', encoding="utf-8") as output_nodes, open('./csv/publishers_papers.csv', 'w', encoding="utf-8") as output_relationships:
    nodes_writer = csv.writer(output_nodes, quoting=csv.QUOTE_STRINGS)
    relationships_writer = csv.writer(
        output_relationships, quoting=csv.QUOTE_STRINGS)

    for file in os.listdir('./json/papers'):
        with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                if not paper['publicationVenue']:
                    continue

                publisher = paper['publicationVenue']
                paper_id = paper['paperId']
                publisher_id = publisher['id']
                name = publisher['name']
                publisher_type = publisher.get('type', 'unknown')
                date = paper['publicationDate']

                if not publisher_id or not paper_id or not date:
                    continue

                nodes_writer.writerow([
                    publisher_id,
                    name,
                    publisher_type
                ])

                relationships_writer.writerow([
                    publisher_id,
                    paper_id,
                    date
                ])
