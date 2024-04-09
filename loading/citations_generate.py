import os
import csv
import json


def write_citation(citation, writer):
    writer.writerow([
        citation[0],
        citation[1]
    ])


def run_stage():
    with open('./csv/citations.csv', 'w', encoding="utf-8") as output:
        writer = csv.writer(output, quoting=csv.QUOTE_STRINGS)

        for file in os.listdir('./json/citations'):
            with open(f'./json/citations/{file}', 'r', encoding="utf-8") as input:
                data = json.load(input)
                for citation in data:
                    write_citation(citation, writer)
