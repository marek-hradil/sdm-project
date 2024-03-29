LOAD CSV FROM "file:///papers.csv" AS row
MERGE (p:Publication { id: row[0], title: row[1], abstract: row[2], year: toInteger(row[3]), citationCount: toInteger(row[4]) });

CREATE CONSTRAINT PublicationId IF NOT EXISTS
FOR (p:Publication) REQUIRE p.id IS UNIQUE;

LOAD CSV FROM "file:///authors.csv" AS row
MERGE (a:Author { id: row[0], name: row[1] });

CREATE CONSTRAINT AuthorId IF NOT EXISTS
FOR (a:Author) REQUIRE a.id IS UNIQUE;

LOAD CSV FROM "file:///keywords.csv" AS row
MERGE (k:Keyword { id: row[0], name: row[1] });

CREATE CONSTRAINT KeywordId IF NOT EXISTS
FOR (k:Keyword) REQUIRE k.id IS UNIQUE;

LOAD CSV FROM "file:///publishers.csv" AS row
MERGE (p:Publisher { id: row[0], name: row[1], type: row[2] });

CREATE CONSTRAINT PublisherId IF NOT EXISTS
FOR (p:Publisher) REQUIRE p.id IS UNIQUE;

LOAD CSV FROM "file:///editions.csv" AS row
MERGE (e:Edition { id: row[0], type: row[1], date: date(row[2]) });

CREATE CONSTRAINT EditionId IF NOT EXISTS
FOR (e:Edition) REQUIRE e.id IS UNIQUE;

LOAD CSV FROM "file:///citations.csv" AS row
MATCH (source:Publication { id: row[0] })
MATCH (target:Publication { id: row[1] })
MERGE (source)-[:CITED]->(target);

LOAD CSV FROM "file:///authors_papers.csv" AS row
MATCH (a:Author { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (a)-[:AUTHORED { main: toBoolean(row[2]) }]->(p);

LOAD CSV FROM "file:///keywords_papers.csv" AS row
MATCH (k:Keyword { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (k)-[:TAGGED]->(p);

LOAD CSV FROM "file:///publishers_editions.csv" AS row
MATCH (p:Publisher { id: row[0] })
MATCH (e:Edition { id: row[1] })
MERGE (p)-[:ORGANIZED]->(e);

LOAD CSV FROM "file:///editions_papers.csv" AS row
MATCH (e:Edition { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (e)-[:PRESENTED]->(p);

LOAD CSV FROM "file:///reviewers_papers.csv" AS row
MATCH (a:Author { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (a)-[:REVIEWED]->(p);