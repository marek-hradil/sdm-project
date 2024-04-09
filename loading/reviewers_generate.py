import csv
import os
import json
from faker import Faker
from random import randint


fake = Faker()


def remove_lineends(s):
    return (s or '').replace('\n', ' ').replace('\r', ' ')


def append_authors(authors, paper):
    if paper['year'] is None:
        return

    authors.extend(paper['authors'] or [])


def create_reviewers(paper, authors):
    paper_authors = [author['authorId']
                     for author in paper['authors'] or []]
    reviewer_count = randint(3, 6)
    reviewers = []

    while len(reviewers) < reviewer_count:
        reviewer = authors[randint(0, len(authors) - 1)]
        if reviewer['authorId'] not in reviewers and \
                reviewer['authorId'] not in paper_authors:
            reviewers.append(reviewer)

    return reviewers


def write_reviewer(reviewer, paper, writer):
    decision = "Rejected" if randint(0, 9) == 0 else "Accepted"
    writer.writerow([
        reviewer['authorId'],
        paper['paperId'],
        remove_lineends(fake.sentence()),
        decision
    ])


def run_stage():
    with open('./csv/reviewers_papers.csv', 'w', encoding="utf-8") as reviewers_papers_output:
        reviewers_papers_writer = csv.writer(
            reviewers_papers_output, quoting=csv.QUOTE_STRINGS)

        authors = []

        for file in os.listdir('./json/papers'):
            with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
                data = json.load(input)

                for paper in data:
                    append_authors(authors, paper)

        for file in os.listdir('./json/papers'):
            with open(f'./json/papers/{file}', 'r', encoding="utf-8") as input:
                data = json.load(input)

                for paper in data:
                    if paper['year'] is None:
                        continue

                    reviewers = create_reviewers(paper, authors)

                    for reviewer in reviewers:
                        write_reviewer(reviewer, paper,
                                       reviewers_papers_writer)
