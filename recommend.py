from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    with open('./recommender/database_community.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')

        print(f'--- Chosen keywords ({len(records)}) ---')
        for record in records:
            print('- ' + record['keyword']['name'])

    with open('./recommender/publications_community.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')

        print(f'--- Related journals ({len(records)}) ---')
        for record in records:
            print('- ' + record['publisher']['name'])

    with open('./recommender/top100.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')

        print(
            f'--- Top 100 papers among the publishers ({len(records[0]['topPapers'])}) ---')
        for record in records[0]['topPapers']:
            print(f'- {record['paper']['title']} : {
                  record['numCitations']}')

    with open('./recommender/gurus.cypher') as file:
        records, _, _ = driver.execute_query(file.read(), database='neo4j')

        print(f'--- Good potential reviewers ({len(records)}) ---')
        for record in records:
            print('- ' + record['guru']['name'])
