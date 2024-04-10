//The first thing to do is to find/define the research communities. A community is
//defined by a set of keywords. Assume that the database community is defined through
//the following keywords: data management, indexing, data modeling, big data, data
//processing, data storage and data querying
MATCH (keyword:Keyword)
WHERE keyword.name IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
RETURN keyword

