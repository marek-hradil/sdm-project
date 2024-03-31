// Define the keywords representing the research communities
MATCH (k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']

MATCH (k)-[:TAGGED]->(p:Publication)<-[c:CITED]-(other:Publication)

WITH k.name AS Keyword, p, COUNT(c) AS numCitations

// Return the top 100 papers with the highest number of citations for each keyword
ORDER BY numCitations DESC
LIMIT 100
RETURN Keyword, p AS TopPaper, numCitations AS NumberOfCitations
