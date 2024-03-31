CALL gds.graph.project(
'publications',
'Publication',
'CITED'
)
YIELD graphName, nodeCount;
