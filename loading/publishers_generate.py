import os
import json
import csv
from uuid import uuid4

with open('./csv/publishers.csv', 'w', encoding="utf-8") as output_publishers, \
        open('./csv/publishers_editions.csv', 'w', encoding="utf-8") as output_publishers_editions, \
        open('./csv/editions_papers.csv', 'w', encoding="utf-8") as output_editions_papers, \
        open('./csv/editions.csv', 'w', encoding="utf-8") as output_editions:

    publishers_writer = csv.writer(
        output_publishers, quoting=csv.QUOTE_STRINGS)
    publishers_editions_writer = csv.writer(
        output_publishers_editions, quoting=csv.QUOTE_STRINGS)
    editions_papers_writer = csv.writer(
        output_editions_papers, quoting=csv.QUOTE_STRINGS)
    editions_writer = csv.writer(
        output_editions, quoting=csv.QUOTE_STRINGS)

    publishers = dict()

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

                current_publisher = publishers.get(publisher_id, {
                    'id': publisher_id,
                    'name': name,
                    'type': publisher_type,
                    'editions': []
                })

                editions = current_publisher['editions']
                editions_dates = [edition['date'] for edition in editions]

                if date in editions_dates:
                    index = editions_dates.index(date)
                    editions[index]['paper_ids'].append(paper_id)
                else:
                    editions.append({
                        'id': uuid4(),
                        'date': date,
                        'type': 'volume' if publisher_type == 'journal' else 'edition',
                        'paper_ids': [paper_id],
                    })

                current_publisher['editions'] = editions
                publishers[publisher_id] = current_publisher

    for publisher_id, publisher in publishers.items():
        publishers_writer.writerow([
            publisher_id,
            publisher['name'],
            publisher['type'],
        ])

        for edition in publisher['editions']:
            editions_writer.writerow([
                edition['id'],
                edition['type'],
                edition['date'],
            ])

            publishers_editions_writer.writerow([
                publisher_id,
                edition['id'],
            ])

            for paper_id in edition['paper_ids']:
                editions_papers_writer.writerow([
                    edition['id'],
                    paper_id,
                ])
