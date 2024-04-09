import os
import csv
import json
from random import randint
from uuid import uuid4
from faker import Faker

fake = Faker()


def append_authors(authors, paper):
    for index, author in enumerate(paper['authors'] or []):
        author_id = author.get('authorId', None)
        name = author['name']
        main_author = index == 0

        if not author_id or not name:
            continue

        current_author = authors.get(author_id, {
            'id': author_id,
            'name': name,
            'paper_ids': [],
        })
        current_author['paper_ids'].append(
            (paper['paperId'], main_author))
        authors[author_id] = current_author


def create_affiliations(authors):
    affiliations = []
    for _ in range(len(authors)):
        affiliation_type = 'University' if randint(0, 1) == 0 else 'Company'
        name = fake.company() if affiliation_type == 'Company' else fake.name() + ' University'

        affiliations.append({
            'id': uuid4(),
            'name': name,
            'type': affiliation_type,
        })

    linkings = dict()
    for author in authors.values():
        linkings[author['id']
                 ] = affiliations[randint(0, len(affiliations) - 1)]

    return affiliations, linkings


def write_affiliation(affiliation, affiliations_writer):
    affiliations_writer.writerow([
        affiliation['id'],
        affiliation['name'],
        affiliation['type'],
    ])


def write_author(author, writer):
    writer.writerow([
        author['id'],
        author['name'],
    ])


def write_affiliation_link(author, authors_affiliations, writer):
    writer.writerow([
        authors_affiliations[author['id']]['id'],
        author['id'],
    ])


def write_author_papers_link(author, writer):
    for paper_id, main_author in author['paper_ids']:
        writer.writerow([
            author['id'],
            paper_id,
            'Main' if main_author else 'Coauthor',
        ])


def run_stage():
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

        authors = dict()

        for file in os.listdir('./json/papers'):
            with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
                data = json.load(input)

                for paper in data:
                    append_authors(authors, paper)

        affiliations, authors_affiliations = create_affiliations(authors)

        for affiliation in affiliations:
            write_affiliation(affiliation, affiliations_writer)

        for author in authors.values():
            write_author(author, authors_writer)
            write_affiliation_link(author, authors_affiliations,
                                   affiliations_authors_writer)
            write_author_papers_link(author, authors_papers_writer)
