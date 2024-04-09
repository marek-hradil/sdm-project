from neo4j import GraphDatabase
from datetime import datetime

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    records, _, _ = driver.execute_query(
        "CALL gds.graph.list('publications') YIELD graphName", database_='neo4j')

    if len(records) == 0:
        with open('./graph/setup.cypher') as file:
            driver.execute_query(file.read(), database_='neo4j')

    with open('./graph/sc_components.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database_='neo4j')

        print('--- Strongly connected components:')
        for record in records:
            print(f'\t - {record['publication']['title']}')

    with open('./graph/communities.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database_='neo4j')

        print('--- Communities:')

        for record in records:
            print(f'\t - Community {record['community']['id']}')
            for publication in record['publications']:
                print(f'\t\t - {publication['title']}')

        driver.execute_query(
            'MATCH (c:Community) DETACH DELETE c;', database_='neo4j')
