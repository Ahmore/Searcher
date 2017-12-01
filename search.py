import argparse
import time

from engine.search import Search

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--index", type=str, required=True)
    args = parser.parse_args()

    search = Search(args.index)

    print("[Searching]")
    st = time.time()
    results = search.eval(args.query, args.n)

    print("[Results]")
    for i in range(len(results)):
        print(results[i]["url"])

    print("--- %s seconds ---" % (time.time() - st))