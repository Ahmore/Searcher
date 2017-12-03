To test searcher:

Run spider to download data:\
scrapy crawl wikispider

Run index with interesting configuration
python index.py --input="documents/wikidocuments1512165413.json" --n=1000 -idf -lra --k=900 --output="indexes/wikiindex_1000_lra_900.json"

Run server
...

Enjoy