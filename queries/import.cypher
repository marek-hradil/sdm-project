LOAD CSV FROM "file:///papers.csv" AS row
MERGE (p:Publication { id: row[0], title: row[1], abstract: row[2], year: toInteger(row[3]), citationCount: toInteger(row[4]) })
RETURN
p.id AS id,
p.title AS title,
p.abstract AS abstract,
p.year AS year,
p.citationCount AS citationCount
LIMIT 5

CREATE CONSTRAINT PublicationId IF NOT EXISTS
FOR (p:Publication) REQUIRE p.id IS UNIQUE

LOAD CSV FROM "file:///authors.csv" AS row
MERGE (a:Author { id: row[0], name: row[1] })
RETURN
a.id AS id,
a.name AS name
LIMIT 5

CREATE CONSTRAINT AuthorId IF NOT EXISTS
FOR (a:Author) REQUIRE a.id IS UNIQUE

LOAD CSV FROM "file:///keywords.csv" AS row
MERGE (k:Keyword { id: row[0], keyword: row[1] })
RETURN
k.id AS id,
k.keyword AS keyword
LIMIT 5

CREATE CONSTRAINT KeywordId IF NOT EXISTS
FOR (k:Keyword) REQUIRE k.id IS UNIQUE

LOAD CSV FROM "file:///publishers.csv" AS row
MERGE (p:Publisher { id: row[0], name: row[1], type: row[2] })
RETURN
p.id AS id,
p.name AS name,
p.type AS type
LIMIT 5

CREATE CONSTRAINT PublisherId IF NOT EXISTS
FOR (p:Publisher) REQUIRE p.id IS UNIQUE

LOAD CSV FROM "file:///editions.csv" AS row
MERGE (e:Edition { id: row[0], type: row[1], date: toDate(row[2]) })
RETURN
e.id AS id,
e.type AS type,
e.date AS date
LIMIT 5

CREATE CONSTRAINT EditionId IF NOT EXISTS
FOR (e:Edition) REQUIRE e.id IS UNIQUE

LOAD CSV FROM "file:///citations.csv" AS row
MATCH (source:Publication { id: row[0] })
MATCH (target:Publication { id: row[1] })
MERGE (source)-[:CITED]->(target)
RETURN
source.id AS source,
target.id AS target
LIMIT 5

LOAD CSV FROM "file:///authors_papers.csv" AS row
MATCH (a:Author { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (a)-[:AUTHORED { main: toBoolean(row[2]) }]->(p)
RETURN
a.id AS author,
p.id AS publication
LIMIT 5

LOAD CSV FROM "file:///keywords_papers.csv" AS row
MATCH (k:Keyword { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (k)-[:TAGGED]->(p)
RETURN
k.id AS keyword,
p.id AS publication
LIMIT 5

LOAD CSV FROM "file:///publishers_editions.csv" AS row
MATCH (p:Publisher { id: row[0] })
MATCH (e:Edition { id: row[1] })
MERGE (p)-[:ORGANIZED]->(e)
RETURN
p.id AS publisher,
e.id AS edition
LIMIT 5

LOAD CSV FROM "file:///editions_papers.csv" AS row
MATCH (e:Edition { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (e)-[:PRESENTED]->(p)
RETURN
e.id AS edition,
p.id AS publication
LIMIT 5

LOAD CSV FROM "file:///reviewers_papers.csv" AS row
MATCH (a:Author { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (a)-[:REVIEWED]->(p)
RETURN
a.id AS reviewer,
p.id AS publication
LIMIT 5
