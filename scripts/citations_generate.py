import os
import json

with open('./csv/citations.csv', 'w', encoding="utf-8") as output:
    for file in os.listdir('./json/citations'):
        with open(f'./json/citations/{file}', 'r', encoding="utf-8") as input:
            data = json.load(input)

            for paper in data:
                for citation in paper['citations']:
                    if not citation['paperId']:
                        continue

                    row = [
                        paper['paperId'],
                        citation['paperId']
                    ]

                    output.write(
                        ','.join(row) + '\n'
                    )
