import argparse

import time
from eve import Eve
import json

from engine.search import Search

app = Eve()

# Search engine
search_engine = None


@app.route('/search/<query>', defaults={"n": 10})
@app.route('/search/<query>/<n>')
def search(query, n):
    start_time = time.time()
    results = search_engine.eval(query, int(n))

    return json.dumps({
        "results": results,
        "time": time.time() - start_time
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=str, required=True)
    args = parser.parse_args()

    st = time.time()
    print("[Loading index]")
    search_engine = Search(args.index)
    print("--- %s seconds ---" % (time.time() - st))

    app.run()
