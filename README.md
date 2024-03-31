## How to log into the DB

1. `docker-compose up`
2. After it runs, go to `http://localhost:7474/`
3. Leave the database name empty, username is `neo4j`, password is `password`
4. Connect

## How to clear the database

1. Go to the main folder and stop the running databse
2. Run `sudo rm -rf ./data ./logs` and fill in the password
3. Run `docker-compose up --build` again

## Data

We are using `https://www.semanticscholar.org/`.

## TODO list

### A.1

- Starting the lab paper
- Deciding the schema of DB

### A.2

- Creating the bulk create script

### A.3

- Decide the changes to the schema
- Create the migration script
- Modify the lab paper

### B

- Queries
  - For each conference, top 3 cited papers
  - For each conference, find stable authors
    - "stable" - paper for atleast 4 different editions
  - For each journal and each year, Impact Factor
    - Impact Factor for year X = (citations in year X of publications in years X-1 and X-2) / (publications in years X-1 and X-2)
  - For each author, h-index
    - h-index = maximum value of h such that the given author has published h papers that have each been cited at least h times

### C

- Recommender for reviewer
  - Given community (set of keywords)
  - Find related conferences and journals for the community
    - 90% of published papers contain atleast one of the keyword
  - Top papers of community
    - Top 100 papers of the related conferences/journals to that community, by citations
  - Authors of the top papers
    - Author of any of the top 100 papers
  - Gurus of the top papers
    - Author of atleast two top 100 papers

### D

- Choose two algorithms and apply them

## Initialization instructions

### Requirements

- Docker
- python (ideally v.12)
- some python package installer (conda, pip, ...)

### First startup

- Download required python packages (should be yake, thefuzz and maybe requests if not already included in base libraries)
- Create empty `json` and `csv` folders
- Running `./download_all.sh` should be enough (if not runnable, go for `chmod +x ./download_all.sh`)
- After database starts, interface should be available at `localhost:7474`
- There, run the `./queries/import.cypher` script

### Next startups

- Running `docker compose up` should be enough
