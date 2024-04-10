//Next, we need to find the conferences and journals related to the database community
//(i.e., are specific to the field of databases).
//Assume that if 90% of the papers published in a conference/journal contain one of the keywords of the database community we
//consider that conference/journal as related to that community.

//Find the publications tagged with specified keywords
MATCH (k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
MATCH (k)-[:TAGGED]->(pub:Publication)

// Find publications for publishers
MATCH (p:Publisher)-[:ORGANIZED]->(edition:Edition)-[:PRESENTED]->(pub)

// Count the number of publications for each publisher
WITH p AS publisher, COUNT(pub) AS totalPublications, COLLECT(pub) AS allPublications

// Count the number of publications tagged with specified keywords for each //publisher
MATCH (p)-[:ORGANIZED]->(edition:Edition)-[:PRESENTED]->(pub)<-[:TAGGED]-(k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
WITH publisher, totalPublications, COUNT(pub) AS taggedPublications, allPublications

// Check if at least 90% of tagged publications are included in all publications
WITH publisher, totalPublications, taggedPublications, allPublications,
taggedPublications * 1.0 / totalPublications AS taggedRatio
WHERE taggedRatio >= 0.9

RETURN publisher
