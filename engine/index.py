import numpy as np
import scipy.sparse

from engine import jsonstorage, stringparser
from engine.normalizer import Normalizer


class Index:
    def __init__(self, documents, filename):
        self.documents = documents
        self.dictionary = []
        self.matrix = []

        # Init parser
        self.parser = stringparser.StringParser()

        # Init storage
        self.storage = jsonstorage.JSONStorage(filename)

    def init_dictionary(self):
        for key in self.documents:
            self.documents[key]["words"] = self.parser.parse(self.documents[key]["content"])

        for key in self.documents:
            for word in self.documents[key]["words"]:
                self.dictionary.append(word)

        # Dictionary without duplicates and limited to dictionary
        self.dictionary = list(set(self.dictionary).intersection(self.parser.nltk_words))

    def create_index(self):
        matrix = np.zeros((len(self.documents), len(self.dictionary)))
        i = 0

        for key in self.documents:
            for word in self.documents[key]["words"]:
                if word in self.dictionary:
                    matrix[i][self.dictionary.index(word)] += 1
            i += 1

        self.matrix = scipy.sparse.csc_matrix(matrix)

    def idf(self):
        words_amount = len(self.dictionary)
        documents_amount = len(self.documents)

        for i in range(words_amount):
            nw = self.matrix[:, i].getnnz()
            self.matrix[:, i] *= np.math.log(documents_amount / nw)

    def lra(self, k):
        u, s, v = scipy.sparse.linalg.svds(self.matrix, k=k)

        self.matrix = scipy.sparse.csc_matrix(np.asmatrix(u) * np.asmatrix(np.diag(s)) * np.asmatrix(v))

    def normalize(self):
        Normalizer.normalize(self.matrix.tocsr())

    def save(self):
        data = {
            "dictionary": self.dictionary,
            "documents": [{"url": self.documents[key]["url"], "title": self.documents[key]["title"]} for key in self.documents],
            "matrix": self.matrix.toarray().tolist()
        }

        self.storage.save(data)