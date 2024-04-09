// Find the top 3 most cited papers of each conference

MATCH (publisher:Publisher { type: "conference" })-[:ORGANIZED]->(edition:Edition)
-[:PRESENTED]->(publication:Publication)<-[:CITED]-(citingPublication:Publication)
WITH publisher, publication, count(citingPublication) AS citationCount
 ORDER BY citationCount DESC
WITH COLLECT(publication) AS publications, publisher
RETURN publisher AS conference, publications[0..3] AS publications
