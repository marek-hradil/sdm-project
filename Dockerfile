FROM neo4j:5

ADD csv/* /var/lib/neo4j/import/

# RUN neo4j-admin database import full \
#     --id-type string \
#     --strict \
#     --verbose \
#     --nodes=Publication=import/papers_header.csv,import/papers.csv \
#     --nodes=Author=import/authors_header.csv,import/authors.csv \
#     --nodes=Keyword=import/keywords_header.csv,import/keywords.csv \
#     --nodes=Publisher=import/publishers_header.csv,import/publishers.csv \
#     --relationships=CITED=import/citations_header.csv,import/citations.csv \
#     --relationships=AUTHORED=import/authors_papers_header.csv,import/authors_papers.csv \
#     --relationships=IS_INCLUDED_IN=import/keywords_papers_header.csv,import/keywords_papers.csv \
#     --relationships=PUBLISHED=import/publishers_papers_header.csv,import/publishers_papers.csv neo4j


