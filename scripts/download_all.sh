echo "--- Starting the download of data 🚀 ..."

python ./scripts/papers_download.py

echo "--- Download finished, continuing to parsing to csv 📦 ..."

python ./scripts/papers_generate.py
python ./scripts/authors_generate.py
python ./scripts/citations_generate.py
python ./scripts/keywords_generate.py
python ./scripts/publishers_generate.py

echo "--- Parsing finished, now making files unique 🧹 ..."

chmod +x ./uniq.sh

./uniq.sh authors
./uniq.sh citations
./uniq.sh keywords
./uniq.sh publishers
./uniq.sh papers

echo "--- Making files unique finished, now spinning up the db 🛢️"

docker compose up --build