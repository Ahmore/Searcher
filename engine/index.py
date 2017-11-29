import json
import string
from nltk.corpus import words as nltk_words
import numpy as np
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem.porter import PorterStemmer
import re


class Index:
    def __init__(self, documents):
        self.documents = documents
        self.dictionary = []
        self.matrix = []

        # Download stopwords
        nltk.download('stopwords')
        nltk.download('words')

        # Words and stopwords
        self.nltk_words = nltk_words.words()
        self.nltk_stopwords = nltk_stopwords.words('english')

        # Init stemmers
        self.porter_stemmer = PorterStemmer()

    def init_dictionary(self):
        for key in self.documents:
            words = self.get_words(self.documents[key]["content"])
            parsed_words = []

            for word in words:
                # Parsing
                word = self.clear_words_from_unicode(word)
                word = self.clear_words_from_punctuation(word)
                word = self.other_clear(word)

                # Filtering
                if not (self.is_empty(word) or self.is_stop_words(word)):
                    # Stemming
                    word = self.use_porter_stemmer(word)

                    # Check if is in english dictionary
                    if word in self.nltk_words:
                        parsed_words.append(word)

            self.documents[key]["words"] = parsed_words

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

            if nw > 0:
                for j in range(documents_amount):
                    self.matrix[j][i] *= np.math.log(documents_amount / nw)

            i += 1

    def save_to_json(self, filename):
        data = {
            "dictionary": self.dictionary,
            "documents": [{"url": self.documents[key]["url"], "title": self.documents[key]["title"]} for key in self.documents],
            "matrix": self.matrix.tolist()
        }

        with open(filename, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def get_words(content):
        splitted = [words.split(" ") for words in content]
        flat_list = [item.strip().lower() for sublist in splitted for item in sublist]

        return flat_list

    @staticmethod
    def clear_words_from_unicode(word):
        return re.sub(r'(\\u[0-9A-Fa-f]+)', lambda c: "", word)

    @staticmethod
    def clear_words_from_punctuation(word):
        return word.translate(str.maketrans("", "", string.punctuation))

    @staticmethod
    def other_clear(word):
        return re.sub(r'(\n+)', lambda c: "", word)

    @staticmethod
    def is_empty(word):
        return word == ""

    def is_stop_words(self, word):
        return word in self.nltk_stopwords

    def use_porter_stemmer(self, word):
        return self.porter_stemmer.stem(word)