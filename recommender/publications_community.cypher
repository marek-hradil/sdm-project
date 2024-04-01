//Next, we need to find the conferences and journals related to the database community
//(i.e., are specific to the field of databases). 
//Assume that if 90% of the papers published in a conference/journal contain one of the keywords of the database community we
//consider that conference/journal as related to that community.


//Define the keywords representing the research community
MATCH (k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']

// For each keyword, find publications associated with it
MATCH (k)-[:TAGGED]->(p:Publication)

// Collect the publications for each keyword
WITH k, COLLECT(p) AS publications

// Return the keyword along with its associated publications
RETURN k AS Keyword, publications AS Publications
