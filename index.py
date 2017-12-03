import argparse

import time

from engine.index import Index
from engine.jsonstorage import JSONStorage


def slice_dict(dictionary, n):
    result = {}

    for key in dictionary:
        if len(result) < n:
            result[key] = dictionary[key]
        else:
            break

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("-idf", help="Use IDF", action='store_true')
    parser.add_argument("-lra", help="Use LRA", action='store_true')
    parser.add_argument("--k", type=int)
    args = parser.parse_args()

    start_time = time.time()

    print("[Loading documents from JSON]")
    storage = JSONStorage(args.input)
    st = time.time()
    documents = slice_dict(storage.load()["documents"], args.n)
    print("--- %s seconds ---" % (time.time() - st))

    print("")

    print("[Indexing]")
    index = Index(documents, args.output)

    print("")

    print("[Creating dictionary]")
    st = time.time()
    index.init_dictionary()
    print("--- %s seconds ---" % (time.time() - st))

    print("")

    print("[Creating index]")
    st = time.time()
    index.create_index()
    print("--- %s seconds ---" % (time.time() - st))

    print("")

    if args.idf:
        print("[IDF]")
        st = time.time()
        index.idf()
        print("--- %s seconds ---" % (time.time() - st))

        print("")

    if args.lra:
        print("[LRA]")
        st = time.time()
        index.lra(args.k)
        print("--- %s seconds ---" % (time.time() - st))

        print("")

    print("[Normalizing]")
    st = time.time()
    index.normalize()
    print("--- %s seconds ---" % (time.time() - st))

    print("")

    print("[Saving]")
    st = time.time()
    index.save()
    print("--- %s seconds ---" % (time.time() - st))

    print("")

    print("Documents: %d" % len(index.documents))
    print("Words in dictionary: %d" % len(index.dictionary))
    print("--- %s seconds ---" % (time.time() - start_time))
