LOAD CSV FROM "file: ///papers.csv" AS row
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

LOAD CSV FROM "file: ///authors.csv" AS row
MERGE (a:Author { id: row[0], name: row[1] })
RETURN
a.id AS id,
a.name AS name
LIMIT 5

CREATE CONSTRAINT AuthorId IF NOT EXISTS
FOR (a:Author) REQUIRE a.id IS UNIQUE

LOAD CSV FROM "file: ///keywords.csv" AS row
MERGE (k:Keyword { id: row[0], keyword: row[1] })
RETURN
k.id AS id,
k.keyword AS keyword
LIMIT 5

CREATE CONSTRAINT KeywordId IF NOT EXISTS
FOR (k:Keyword) REQUIRE k.id IS UNIQUE

LOAD CSV FROM "file: ///publishers.csv" AS row
MERGE (p:Publisher { id: row[0], name: row[1], type: row[2] })
RETURN
p.id AS id,
p.name AS name,
p.type AS type
LIMIT 5

CREATE CONSTRAINT PublisherId IF NOT EXISTS
FOR (p:Publisher) REQUIRE p.id IS UNIQUE

LOAD CSV FROM "file: ///citations.csv" AS row
MATCH (source:Publication { id: row[0] })
MATCH (target:Publication { id: row[1] })
MERGE (source)-[:CITED]->(target)
RETURN
source.id AS source,
target.id AS target
LIMIT 5

LOAD CSV FROM "file: ///authors_papers.csv" AS row
MATCH (a:Author { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (a)-[:AUTHORED]->(p)
RETURN
a.id AS author,
p.id AS publication
LIMIT 5

LOAD CSV FROM "file: ///keywords_papers.csv" AS row
MATCH (k:Keyword { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (k)-[:TAGGED]->(p)
RETURN
k.id AS keyword,
p.id AS publication
LIMIT 5

LOAD CSV FROM "file: ///publishers_papers.csv" AS row
MATCH (p:Publisher { id: row[0] })
MATCH (p:Publication { id: row[1] })
MERGE (p)-[:PUBLISHED { date: row[2] }]->(p)
RETURN
p.id AS publisher,
p.id AS publication,
row[2] AS date
LIMIT 5
