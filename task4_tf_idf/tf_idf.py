import math

from nltk.corpus import stopwords

import task3_index.index_search as index_search
from settings import *


class TfIdfIndex:
    def __init__(self):

        self.sentences = index_search.token_and_lemma.get_sentences_from_dir(TASK1_OUTPUT_PATH)
        self.tokens = index_search.token_and_lemma.get_tokens(TASK2_PATH + TOKENS_FILENAME)
        print('Started index creation')
        self.tf = {}
        self.df = {}
        self.idf = {}
        print('1/8')
        self.filenames = [ele[0] for ele in self.sentences]
        print('2/8')
        self.file_to_terms = self.process_files()
        print('3/8')
        self.regdex = self.reg_index()
        print('4/8')
        self.totalIndex = self.execute()
        print('5/8')
        self.vectors = self.vectorize()
        print('6/8')
        self.mags = self.magnitudes(self.filenames)
        print('7/8')
        self.populate_scores()
        print('8/8')
        self.save_tf_idf()
        print('Ended')

    def save_tf_idf(self):
        with open('task4_tf_idf/tf_idf.txt', 'w', encoding='utf-8') as file:
            for ele in self.df.keys():
                file.write(f'{ele} {self.df[ele]} {self.df[ele] * self.idf[ele]}\n')

    def process_files(self):
        files_words = [[ele[0], ele[1].split()] for ele in self.sentences]

        temp = {}
        english_stopwords = stopwords.words("english")
        for ele in files_words:
            temp[ele[0]] = []
            for word in ele[1]:
                if word not in english_stopwords:
                    for token in self.tokens.keys():
                        if word in self.tokens[token]:
                            temp[ele[0]].append(token)
                            break
        return temp

    @staticmethod
    def index_one_file(termlist):
        file_index = {}
        for index, word in enumerate(termlist):
            if word in file_index.keys():
                file_index[word].append(index)
            else:
                file_index[word] = [index]
        return file_index

    def make_indices(self, termlists):
        total = {}
        for filename in termlists.keys():
            total[filename] = self.index_one_file(termlists[filename])
        return total

    def vectorize(self):
        vectors = {}
        for filename in self.filenames:
            vectors[filename] = [len(self.regdex[filename][word]) for word in self.regdex[filename].keys()]
        return vectors

    def document_frequency(self, term):
        if term in self.totalIndex.keys():
            return len(self.totalIndex[term].keys())
        else:
            return 0

    def collection_size(self):
        return len(self.filenames)

    def magnitudes(self, documents):
        mags = {}
        for document in documents:
            mags[document] = pow(sum(map(lambda x: x ** 2, self.vectors[document])), .5)
        return mags

    def term_frequency(self, term, document):
        return self.tf[document][term] / self.mags[document] if term in self.tf[document].keys() else 0

    def full_index(self):
        total_index = {}
        indie_indices = self.regdex
        for filename in indie_indices.keys():
            self.tf[filename] = {}
            for word in indie_indices[filename].keys():
                self.tf[filename][word] = len(indie_indices[filename][word])
                if word in self.df.keys():
                    self.df[word] += 1
                else:
                    self.df[word] = 1
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        # noinspection PyTypeChecker
                        total_index[word][filename].append(indie_indices[filename][word][:])
                    else:
                        total_index[word][filename] = indie_indices[filename][word]
                else:
                    total_index[word] = {filename: indie_indices[filename][word]}
        return total_index

    def populate_scores(self):  # pretty sure that this is wrong and makes little sense.
        for filename in self.filenames:
            for term in self.get_uniques():
                self.tf[filename][term] = self.term_frequency(term, filename)
                if term in self.df.keys():
                    self.idf[term] = self.idf_func(self.collection_size(), self.df[term])
                else:
                    self.idf[term] = 0
        return self.df, self.tf, self.idf

    @staticmethod
    def idf_func(n, n_t):
        if n_t != 0:
            return math.log(n / n_t)
        else:
            return 0

    def generate_score(self, term, document):
        return self.tf[document][term] * self.idf[term]

    def get_uniques(self):
        return self.totalIndex.keys()

    def reg_index(self):
        return self.make_indices(self.file_to_terms)

    def execute(self):
        return self.full_index()
