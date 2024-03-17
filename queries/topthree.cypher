#Find the top 3 most cited papers of each conference

MATCH (n: Publication {type: 'conference'})
WITH n ORDER BY n.citationCount desc
WITH n.publicationVenue as conference, collect(n.title) as paper
return conference, paper[0..3]
order by conference
