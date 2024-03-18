#Find the h-indexes of the authors in your graph
#h-index = the number of publications with a citation number greater than or equal to h.
MATCH (a:Author)-[:Wrote]->(p:Publication)
WITH a, p, SIZE((p)<- [:Cites]- ()) AS citations
ORDER BY citations DESC
WITH a, COLLECT(citations) AS citationsList
UNWIND RANGE(0, SIZE(citationsList) - 1) AS idx
WITH a, citationsList, idx
WHERE citationsList[idx] >= idx + 1
WITH a, MAX(idx) + 1 AS hIndex
RETURN a AS Author, hIndex 