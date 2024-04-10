from neo4j import GraphDatabase
from datetime import datetime

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")


def log(text):
    print(f'[{datetime.now()}]: {text}')


with GraphDatabase.driver(URI, auth=AUTH) as driver, open('./evolving/evolve.cypher') as file:
    log('Connected to DB')
    driver.verify_connectivity()
    queries = file.read().split(';')[:-1]
    for query in queries:
        driver.execute_query(query + ';', database='neo4j')
    log('Evolve query executed')
