#For each conference find its community: i.e., those authors that have published papers
#on that conference in, at least, 4 different editions.
MATCH (a:Author) - [:Wrote]->(p:Publication)-[:publishedin]->(c:Publisher {type: "conference"})
WITH a, c, COUNT(DISTINCT c.edition_name) AS editions
WHERE editions >= 4
RETURN c AS Publisher, COLLETC(a) AS Community