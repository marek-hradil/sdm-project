//Next, we need to find the conferences and journals related to the database community
//(i.e., are specific to the field of databases). 
//Assume that if 90% of the papers published in a conference/journal contain one of the keywords of the database community we
//consider that conference/journal as related to that community.

//Find the publications tagged with specified keywords
MATCH (k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
MATCH (k)<-[:TAGGED]-(pub:Publication)

// Find publications for publishers
MATCH (p:Publisher)-[:ORGANIZED]->(edition:Edition)-[:PRESENTED]->(pub)

// Count the number of publications for each publisher
WITH p AS Publisher, COUNT(pub) AS TotalPublications, COLLECT(pub) AS AllPublications

// Count the number of publications tagged with specified keywords for each //publisher
MATCH (p)-[:ORGANIZED]->(edition:Edition)-[:PRESENTED]->(pub)-[:TAGGED]->(k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
WITH Publisher, TotalPublications, COUNT(pub) AS TaggedPublications, AllPublications

// Check if at least 90% of tagged publications are included in all publications
WITH Publisher, TotalPublications, TaggedPublications, AllPublications,
     TaggedPublications * 1.0 / TotalPublications AS TaggedRatio
WHERE TaggedRatio >= 0.9

RETURN Publisher
