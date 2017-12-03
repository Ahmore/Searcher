To test searcher:

Run spider to download data:
cd search_backend
scrapy crawl wikispider

Run index with interesting configuration
cd search_backend
python index.py --input="documents/wikidocuments1512165413.json" --n=1000 -idf -lra --k=900 --output="indexes/wikiindex_1000_lra_900.json"

Run server
cd search_backend
python server.py --index="indexes/wikiindex_10000_no_lra.json"

Run client
cd search_frontend
gulp serve