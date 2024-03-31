CALL gds.scc.stream('publications')
YIELD nodeId, componentId
WITH componentId, count(*) AS componentSize, collect(gds.util.asNode(nodeId)) AS publications
WHERE componentSize > 1
UNWIND publications AS p
RETURN p;
