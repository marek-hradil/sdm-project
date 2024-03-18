#Find the impact factors of the journals in your graph
#date 2024
MATCH (a:Publication)-[:PublishedIn]->(b:Publisher)
WHERE a.year >= (2024 - 2) AND a.year <= 2024 // Assuming you're calculating for 2024
WITH j, a
OPTIONAL MATCH (cited:Publication)-[:Cites]->(a)
WHERE cited.year = 2024
WITH j, COUNT(DISTINCT a) AS publications, COUNT(cited) AS citations
RETURN j AS Publisher, citations * 1.0 / publications AS ImpactFactor