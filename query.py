from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    with open('./queries/findcommunity.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')

        print('--- Conferences with communities:')
        for record in records:
            publisher = record['publisher']
            print(f'\t{publisher['name']}')
            for author in record['community']:
                print(f'\t\t - {author['name']}')

    with open('./queries/topthree.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')

        print('--- Top three papers for each conference:')
        for record in records:
            conference = record['conference']
            print(f'\t{conference['name']}')
            for publication in record['publications']:
                print(f'\t\t - {publication['title']}')

    with open('./queries/impactfactor.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')

        print('--- Impact factor for each journal:')
        for record in records:
            print(f'\t{record['publisher']['name']} : {
                  record['impactFactor']}')

    with open('./queries/hindex.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')
        print('--- H-Index for each author:')
        for record in records:
            print(f'\t{record['authorName']} : {record['hIndex']}')
