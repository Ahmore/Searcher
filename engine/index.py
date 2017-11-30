import numpy as np
from engine import jsonstorage, stringparser


class Index:
    def __init__(self, documents):
        self.documents = documents
        self.dictionary = []
        self.matrix = []

        # Init parser
        self.parser = stringparser.StringParser()

        # Init storage
        self.storage = jsonstorage.JSONStorage("wikiindex.json")

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

        self.matrix = matrix

    def idf(self):
        documents_amount = len(self.documents)
        i = 0

        for word in self.dictionary:
            nw = len(list(filter(lambda x: (x > 0), self.matrix[:, i])))

            if nw > 0:
                for j in range(documents_amount):
                    self.matrix[j][i] *= np.math.log(documents_amount / nw)

            i += 1

    def save(self):
        data = {
            "dictionary": self.dictionary,
            "documents": [{"url": self.documents[key]["url"], "title": self.documents[key]["title"]} for key in self.documents],
            "matrix": self.matrix.tolist()
        }

        self.storage.save(data)