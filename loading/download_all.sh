echo "--- Starting the download of data 🚀 ..."

python ./loading/papers_download.py

echo "--- Download finished, continuing to parsing to csv 📦 ..."

python ./loading/papers_generate.py
python ./loading/authors_generate.py
python ./loading/citations_generate.py
python ./loading/keywords_generate.py
python ./loading/publishers_generate.py
python ./loading/reviewers_generate.py

echo "--- Parsing finished, now making files unique 🧹 ..."

chmod +x ./uniq.sh

./uniq.sh authors
./uniq.sh citations
./uniq.sh keywords
./uniq.sh publishers
./uniq.sh papers

echo "--- Making files unique finished, now spinning up the db 🛢️"

docker compose up --build