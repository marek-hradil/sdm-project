LOAD CSV FROM 'file:///affiliations.csv' AS row
MERGE (a:Affilation { id: row[0], name: row[1], type: row[2] });

CREATE CONSTRAINT AffiliationId IF NOT EXISTS
FOR (a:Affilation) REQUIRE a.Id IS UNIQUE;

LOAD CSV FROM 'file:///affiliations_authors.csv' AS row
MATCH (af:Affilation { id: row[0] })
MATCH (au:Author { id: row[1] })
MERGE (au)-[:WORKS_AT]->(af);

LOAD CSV FROM 'file:///reviewers_papers.csv' AS row
MATCH (a:Author { id: row[0] })-[r:REVIEWED]->(p:Publication { id: row[1] })
 SET r.content = row[2]
 SET r.decision = row[3];
