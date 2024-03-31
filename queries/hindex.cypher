//Find the h-indexes of the authors in your graph
//h-index = the number of publications with a citation number greater than or equal to h.
MATCH (a:Author)-[:AUTHORED]->(p:Publication)
OPTIONAL MATCH (p)<-[:CITED]-(otherPublication:Publication)
WITH a, p, COUNT(otherPublication) AS citationsCount
 ORDER BY citationsCount DESC
WITH a, COLLECT(citationsCount) AS citationCounts
WITH a, REDUCE(s = 0, count IN RANGE(1, SIZE(citationCounts)) |

CASE WHEN citationCounts[count - 1] >= count THEN count ELSE s END) AS hIndex
RETURN a.name AS AuthorName, hIndex