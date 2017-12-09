import numpy as np
import scipy
import scipy.sparse

from engine import stringparser, jsonstorage
from engine.normalizer import Normalizer


class Search:
    def __init__(self, filename):
        # Init parser
        self.parser = stringparser.StringParser()

        # Init storage
        self.storage = jsonstorage.JSONStorage(filename)

        # Load from storage
        stg = self.storage.load()

        self.dictionary = stg["dictionary"]
        self.documents = stg["documents"]
        self.matrix = scipy.sparse.csc_matrix(stg["matrix"])

    def eval(self, query, n):
        # Parse query words
        words = self.parser.parse([query])

        # Make query vector
        vector = self.create_vector(words)

        # Normalize vector
        Normalizer.normalize(vector)

        # Count similarity of query to each document
        similarity = [np.math.fabs(s) for s in (vector * self.matrix.transpose()).toarray()[0]]

        # Pair documents with theirs vectors
        pairs = []
        for i in range(len(self.documents)):
            pairs.append({
                "document": self.documents[i],
                "similarity": similarity[i]
            })

        # Sort by similarity
        sorted_pairs = sorted(pairs, key=lambda pair: pair["similarity"], reverse=True)

        # Delete similarity from result
        result = list(map(lambda x: x["document"], sorted_pairs))

        # Return n best results
        return result[:n]

    def create_vector(self, words):
        matrix = np.zeros((1, len(self.dictionary)))

        for word in words:
            if word in self.dictionary:
                matrix[0][self.dictionary.index(word)] += 1

        return scipy.sparse.csc_matrix(matrix)



