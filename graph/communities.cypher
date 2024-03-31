CALL gds.louvain.stream('publications') YIELD nodeId, communityId
WITH communityId, nodeId
MERGE (c:Community { id: communityId })
WITH c, nodeId
MATCH (p:Publication { id: gds.util.asNode(nodeId).id })
MERGE (p)-[:BELONGS_TO]->(c)
RETURN c, p;

// MATCH (c:Community) DETACH DELETE c;
