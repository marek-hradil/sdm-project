

// Find publications for publishers
MATCH (p:Publisher)-[:ORGANIZED]->(edition:Edition)-[:PRESENTED]->(pub)

WITH p AS Publisher, COUNT(pub) AS TotalPublications, COLLECT(pub) AS AllPublications

// Count the number of publications tagged with specified keywords for each 
MATCH (p)-[:ORGANIZED]->(edition:Edition)-[:PRESENTED]->(pub)-[:TAGGED]->(k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
WITH Publisher, TotalPublications, COUNT(pub) AS TaggedPublications, AllPublications


WITH Publisher, TotalPublications, TaggedPublications, AllPublications,
     TaggedPublications * 1.0 / TotalPublications AS TaggedRatio
WHERE TaggedRatio >= 0.9

// Return the top 100 most cited papers among all publications associated with the selected publishers
UNWIND AllPublications AS paper
WITH DISTINCT paper
MATCH (paper)<-[c:CITED]-()
WITH paper, COUNT(c) AS numCitations
ORDER BY numCitations DESC
LIMIT 100

RETURN COLLECT({paper: paper, numCitations: numCitations}) AS TopPapers
