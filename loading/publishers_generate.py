import os
import json
import csv
from uuid import uuid4


def append_publishers(publishers, paper):
    publisher = paper['publicationVenue']
    if not publisher:
        return

    paper_id = paper['paperId']
    publisher_id = publisher['id']
    name = publisher['name']
    publisher_type = publisher.get('type', 'unknown')
    date = paper['publicationDate']

    if not publisher_id or not paper_id or not date:
        return

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


def write_publisher(publisher, writer):
    writer.writerow([
        publisher['id'],
        publisher['name'],
        publisher['type'],
    ])


def write_edition(edition, publisher, node_writer, link_writer):
    node_writer.writerow([
        edition['id'],
        edition['type'],
        edition['date'],
    ])

    link_writer.writerow([
        publisher['id'],
        edition['id'],
    ])


def run_stage():
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
                    append_publishers(publishers, paper)

        for _, publisher in publishers.items():
            write_publisher(publisher, publishers_writer)

            for edition in publisher['editions']:
                write_edition(edition, publisher, editions_writer,
                              publishers_editions_writer)

                for paper_id in edition['paper_ids']:
                    editions_papers_writer.writerow([
                        edition['id'],
                        paper_id,
                    ])
