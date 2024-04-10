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

## Initialization instructions

### Requirements

- Docker
- python (ideally v.12)
- some python package installer (conda, pip, ...)
- python packages:
  - neo4j
  - faker
  - thefuzz
  - yake
