import time

import scipy

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


n = 10000
st = time.time()

print("[Loading data from JSON]")
storage = JSONStorage("indexes/wikiindex_10000_no_idf_no_lra.json").load()
documents = slice_dict(JSONStorage("documents/wikidocuments1512339671.json").load()["documents"], n)
print("--- %s seconds ---" % (time.time() - st))

print("")


print("[Testing]")
print("")
for idf in range(2):
    for lra in range(2):
        if idf == 0 and lra == 0:
            continue

        for k in range(7000, 10000, 2000):
            st = time.time()

            print("[Indexing]")
            index = Index(documents, ("indexes/wikiindex_10000_%s_%s.json" %
                                      ("no_idf" if idf == 0 else "idf",
                                      "no_lra" if lra == 0 else ("lra_%d" % k))))

            index.dictionary = storage["dictionary"]
            index.matrix = scipy.sparse.csc_matrix(storage["matrix"])

            print("")

            if idf == 1:
                print("[IDF]")
                st = time.time()
                index.idf()
                print("--- %s seconds ---" % (time.time() - st))

                print("")

            if lra == 1:
                print("[LRA]")
                st = time.time()
                index.lra(k)
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

            if lra == 0:
                break
