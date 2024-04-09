import subprocess
import time
from neo4j import GraphDatabase
from datetime import datetime
from loading import papers_download, papers_generate, citations_generate, authors_generate, keyword_generate, reviewers_generate, publishers_generate


URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")


def log(text):
    print(f'[{datetime.now()}]: {text}')


def load_data():
    print('--- STARTING LOADING DATA ---')
    log('Start paper download')
    papers_download.run_stage()
    log('Start generating papers')
    papers_generate.run_stage()
    log('Start generating citations')
    citations_generate.run_stage()
    log('Start generating authors')
    authors_generate.run_stage()
    log('Start generating keywords')
    keyword_generate.run_stage()
    log('Start generating reviewers')
    reviewers_generate.run_stage()
    log('Start generating publishers')
    publishers_generate.run_stage()
    print('--- DATA GENERATION DONE ---')


def run_db():
    log('Starting database')
    subprocess.run(
        ['docker', 'compose', 'up', '-d', '--build', '--force-recreate']
    )
    log('Wait for the startup')
    time.sleep(60)
    log('Database started')


def connect_db():
    log('Connecting to DB')

    with GraphDatabase.driver(URI, auth=AUTH) as driver, open('./loading/import.cypher') as file:
        log('Connected to DB')
        driver.verify_connectivity()
        queries = file.read().split(';')[:-1]
        for query in queries:
            driver.execute_query(query + ';', database='neo4j')

        log('Import query executed')

    log('Closed connection')
    print('--- DATA LOADED ---')


# load_data()
run_db()
connect_db()
