To test searcher:

Run spider to download data:\
scrapy crawl wikispider

Run index with interesting configuration
python index.py --input="documents/wikidocuments1512165413.json" --n=1000 -idf -lra --k=900 --output="indexes/wikiindex_1000_lra_900.json"

Run server
python server.py --index="indexes/wikiindex_10000_no_lra.json"

Run client
npm start

Enjoy searching...