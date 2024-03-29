WITH ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying'] AS community
UNWIND community AS keyword_value

MATCH (publisher:Publisher)-[:PUBLISHED]->(publication:Publication)<-[:TAGGED]-(keyword:Keyword)
WITH community, publisher, publication, keyword_value
MATCH (publisher)-[:PUBLISHED]->(community_publication: Publication)<-[:TAGGED]-(keyword { keyword: keyword_value })
RETURN publisher, COUNT(publication), COUNT(community_publication)
