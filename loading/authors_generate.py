import os
import csv
import json
from random import randint
from uuid import uuid4
from faker import Faker

fake = Faker()

with open('./csv/authors.csv', 'w', encoding="utf-8") as authors_output, \
        open('./csv/authors_papers.csv', 'w', encoding="utf-8") as authors_papers_output, \
        open('./csv/affiliations.csv', 'w', encoding="utf-8") as affiliations_output, \
        open('./csv/affiliations_authors.csv', 'w', encoding="utf-8") as affiliations_authors_output:
    authors_writer = csv.writer(authors_output, quoting=csv.QUOTE_STRINGS)
    authors_papers_writer = csv.writer(
        authors_papers_output, quoting=csv.QUOTE_STRINGS)
    affiliations_writer = csv.writer(
        affiliations_output, quoting=csv.QUOTE_STRINGS)
    affiliations_authors_writer = csv.writer(
        affiliations_authors_output, quoting=csv.QUOTE_STRINGS)

    authors = []

    for file in os.listdir('./json/papers'):
        with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                for index, author in enumerate(paper['authors'] or []):
                    author_id = author.get('authorId', None)
                    name = author['name']
                    main_author = index == 0

                    if not author_id or not name:
                        continue

                    authors_papers_writer.writerow([
                        author_id,
                        paper['paperId'],
                    ])

                    authors.append({
                        'id': author_id,
                        'name': name,
                        'main': main_author,
                    })

    affiliations = []
    for _ in range(len(authors)):
        affiliation_type = 'University' if randint(0, 1) == 0 else 'Company'
        name = fake.company() if affiliation_type == 'Company' else fake.name() + ' University'

        affiliations.append({
            'id': uuid4(),
            'name': name,
            'type': affiliation_type,
        })

    authors_affiliations = dict()
    for author in authors:
        authors_affiliations[author['id']
                             ] = affiliations[randint(0, len(affiliations) - 1)]

    for affiliation in affiliations:
        affiliations_writer.writerow([
            affiliation['id'],
            affiliation['name'],
            affiliation['type'],
        ])

    for author in authors:
        authors_writer.writerow([
            author['id'],
            author['name'],
            author['main'],
        ])

        affiliations_authors_writer.writerow([
            authors_affiliations[author['id']]['id'],
            author['id'],
        ])
