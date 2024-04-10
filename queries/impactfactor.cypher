//Find the impact factors of the journals in your graph
//date 2024
MATCH (a:Publication)<-[:PRESENTED]-(e:Edition)<-[:ORGANIZED]-(b:Publisher)
WHERE a.year >= 2022 AND a.year <= 2023
WITH b, a
OPTIONAL MATCH (cited:Publication)<-[:CITED]-(a)
WHERE cited.year = 2024
WITH b, COUNT(DISTINCT CASE WHEN a.year = 2022 THEN a END) AS publications2022,
            COUNT(DISTINCT CASE WHEN a.year = 2023 THEN a END) AS publications2023,
            COUNT(cited) AS citations2024
RETURN b AS publisher, 
       (citations2024 * 1.0) / (publications2022 + publications2023) AS impactFactor
ORDER BY impactFactor DESC