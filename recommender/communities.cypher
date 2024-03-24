// Define the keywords representing the research communities
MATCH (k:Keyword)
WHERE k.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']

// For each keyword, find publications associated with it
MATCH (k)-[:IS_INCLUDED_IN]->(p:Publication)

// Collect the publications for each keyword
WITH k, COLLECT(p) AS publications

// Return the keyword along with its associated publications
RETURN k AS Keyword, publications AS Publications