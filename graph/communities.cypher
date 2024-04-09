CALL gds.louvain.stream('publications') YIELD nodeId, communityId
WITH communityId, nodeId
MERGE (community:Community { id: communityId })
WITH community, nodeId
MATCH (publication:Publication { id: gds.util.asNode(nodeId).id })
MERGE (publication)-[:BELONGS_TO]->(community)
RETURN community, COLLECT(publication) AS publications;
