import re
import string

from engine.index import Index
import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

# a = ["aaa addd", "sddd"]
# b = [words.split(" ") for words in a]
# flat_list = [item for sublist in b for item in sublist]
# print(flat_list)
#
# print(" a ")

c = {
    "test": {
        "content": ["aaa addd", "sddd \n", "", "aaa I am you are were !", "caresses", "running"],
        "url": "blabal",
        "title": "tytul"
    },

    "test2": {
        "content": ["running", "This is some \\u03c0 text that has to be cleaned\\u2026! it\\u0027s annoying!"],
        "url": "url2",
        "title": "tytul2"
    }
}

index = Index(c)
index.init_dictionary()
index.create_index()
index.parse_matrix_with_idf()
index.save_to_json("index.json")

# s = 'This is some \\u03c0 text that has to be cleaned\\u2026! it\\u0027s annoying!'
# print(s.encode('utf-8'))
# t = 'R\\u00f3fis\\u00edn'
#
# t1 = re.sub(r'(\\u[0-9A-Fa-f]+)', lambda c: "", t)
# print(t1)

# stringIn = "string.with.punctuation!"
# out = stringIn.maketrans("", stringIn.maketrans("",""), string.punctuation)
# print(out)

# print(re.sub(r'(\\(\\)?u[0-9A-Fa-f]+)', lambda c: "", "\\u201"))
# print(re.sub(r'(u[0-9A-Fa-f]+)', lambda c: "", "gr\u03c3\u03c3k"))
# print("123".isdigit())
# print("123e".isdigit())
# print("123ed".isdigit())


# porter_stemmer = PorterStemmer()
# print(porter_stemmer.stem("histories"))
#
# stemmer2 = SnowballStemmer("english")
# print(stemmer2.stem("histories"))

a = [1, 2, 3]
print(a.index(2))
print(a.index(4))
