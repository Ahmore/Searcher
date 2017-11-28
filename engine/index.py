import json
import string

import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re


class Index:
    filename = "index.json"

    def __init__(self, documents):
        self.documents = documents
        self.dictionary = []
        self.matrix = []

        # Download stopwords
        nltk.download('stopwords')

        # Init stemmers
        self.porter_stemmer = PorterStemmer()

    def init_dictionary(self):
        for key in self.documents:
            content = self.documents[key]["content"]

            words = self.get_words(content)
            words = self.clear_words_from_unicode(words)
            words = self.clear_words_from_punctuation(words)
            words = self.basic_filter(words)
            words = self.remove_numeric(words)
            words = self.remove_stop_words(words)
            words = self.use_porter_stemmer(words)

            self.documents[key]["words"] = words

        for key in self.documents:
            for word in self.documents[key]["words"]:
                self.dictionary.append(word)

        # Dictionary without duplicates
        self.dictionary = list(set(self.dictionary))

    def create_index(self):
        matrix = np.zeros((len(self.documents), len(self.dictionary)))
        i = 0

        for key in self.documents:
            for word in self.documents[key]["words"]:
                if word in self.dictionary:
                    matrix[i][self.dictionary.index(word)] += 1
            i += 1

        self.matrix = matrix

    def parse_matrix_with_idf(self):
        documents_amount = len(self.documents)
        i = 0

        for word in self.dictionary:
            nw = len(list(filter(lambda x: (x > 0), self.matrix[:, i])))

            for j in range(documents_amount):
                self.matrix[j][i] *= np.math.log(documents_amount / nw)

            i += 1

    def save_to_json(self):
        data = {
            "dictionary": self.dictionary,
            "documents": [{"url": self.documents[key]["url"], "title": self.documents[key]["title"]} for key in self.documents],
            "matrix": self.matrix.tolist()
        }

        with open(self.filename, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def get_words(content):
        splitted = [words.split(" ") for words in content]
        flat_list = [item.strip().lower() for sublist in splitted for item in sublist]

        return flat_list

    @staticmethod
    def clear_words_from_unicode(words):
        return [re.sub(r'(\\u[0-9A-Fa-f]+)', lambda c: "", word) for word in words]

    @staticmethod
    def clear_words_from_punctuation(words):
        return [word.translate(str.maketrans("", "", string.punctuation)) for word in words]

    @staticmethod
    def basic_filter(words):
        strings = ["", "\n"]

        return list(filter(lambda x: (x not in strings), words))

    @staticmethod
    def remove_numeric(words):
        return list(filter(lambda x: not x.isdigit(), words))

    @staticmethod
    def remove_stop_words(words):
        return [word for word in words if word not in stopwords.words('english')]

    def use_porter_stemmer(self, words):
        return [self.porter_stemmer.stem(word) for word in words]