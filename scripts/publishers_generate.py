import os
import json

with open('./csv/publishers.csv', 'w', encoding="utf-8") as output_nodes, open('./csv/publishers_papers.csv', 'w', encoding="utf-8") as output_relationships:
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

                output_nodes.write(
                    f"{publisher_id},{name},{publisher_type}\n"
                )

                output_relationships.write(
                    f"{publisher_id},{paper_id},{date}\n"
                )
