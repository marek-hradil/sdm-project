sort ./csv/$1.csv | uniq > ./csv/$1-tmp.csv
mv ./csv/$1-tmp.csv ./csv/$1.csv
