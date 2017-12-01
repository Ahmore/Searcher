import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem.porter import PorterStemmer
import re
import string
from nltk.corpus import brown


class StringParser:
    def __init__(self):
        # Download stopwords
        nltk.download('stopwords')
        nltk.download("brown")

        # Words and stopwords
        self.nltk_words = [word.lower() for word in brown.words()]
        self.nltk_stopwords = nltk_stopwords.words('english')

        # Init stemmers
        self.porter_stemmer = PorterStemmer()

    def parse(self, content):
        words = self.get_words(content)
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

                parsed_words.append(word)

        return parsed_words

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