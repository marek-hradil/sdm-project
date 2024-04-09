from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    with open('./recommender/database_community.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')
