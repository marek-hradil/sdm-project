// For each conference find its community: i.e., those authors that have published papers
// on that conference in, at least, 4 different editions.
MATCH (a:Author)-[:AUTHORED]->(publication:Publication)<-[:PRESENTED]-(edition: Edition)<-[:ORGANIZED]-(c:Publisher { type: "conference" })
WITH a, c, COUNT( DISTINCT edition.date) AS editions
WHERE editions >= 4
RETURN c AS publisher, COLLECT(a) AS community
