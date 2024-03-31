// publications graph needed, if throwing error run the other file

CALL gds.scc.stream('publications')
YIELD nodeId, componentId
WITH *
WHERE nodeId <> componentId
WITH nodeId, componentId
MATCH (p:Publication { id: gds.util.asNode(nodeId).id })
RETURN p;
