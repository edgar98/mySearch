import pickle

import spacy
from nltk.corpus import stopwords

from task2_tokenization import token_and_lemma
from task4_tf_idf.tf_idf import TfIdfIndex
import re
from settings import *


def prepare_query(string, nlp_core=SPACY_CORE):
    nlp = spacy.load(nlp_core)
    words = token_and_lemma.tokenize_text(string)
    res = []
    english_stopwords = stopwords.words('english')
    for word in words:
        doc = nlp(word)
        for token in doc:
            if token.lemma_ not in english_stopwords:
                res.append(token.lemma_)
    return res


class Query:

    def __init__(self):
        backup = None
        try:
            with open('vector.bin', 'rb') as file:
                backup = pickle.load(file)
        except IOError:
            print('Something went wrong')
        self.index = TfIdfIndex() if not backup else backup.index
        self.filenames = self.index.filenames if not backup else backup.filenames
        self.invertedIndex = self.index.totalIndex if not backup else backup.invertedIndex
        self.regularIndex = self.index.regdex if not backup else backup.regularIndex
        if not backup:
            with open('vector.bin', 'wb') as file:
                pickle.dump(self, file)

    def one_word_query(self, word):
        if word in self.invertedIndex.keys():
            return self.rank_results([filename for filename in self.invertedIndex[word].keys()], word)
        else:
            return []

    def free_text_query(self, string):
        result = []
        for word in prepare_query(string):
            result += self.one_word_query(word)
        return self.rank_results(list(set(result)), string)

    def strict_text_query(self, string):
        result = []
        for word in prepare_query(string):
            query = self.one_word_query(word)
            result = list(set(result) & set(query)) if result \
                else set(query)
        return self.rank_results(list(set(result)), string)

    # inputs = 'query string', {word: {filename: [pos1, pos2, ...], ...}, ...}
    # inter = {filename: [pos1, pos2]}
    def phrase_query(self, string):
        prepared_query = prepare_query(string)
        list_of_lists, result = [], []
        for word in prepared_query:
            list_of_lists.append(self.one_word_query(word))
        setted = set(list_of_lists[0]).intersection(*list_of_lists)
        for filename in setted:
            temp = []
            for word in prepared_query:
                temp.append(self.invertedIndex[word][filename][:])
            for i in range(len(temp)):
                for ind in range(len(temp[i])):
                    temp[i][ind] -= i
            if set(temp[0]).intersection(*temp):
                result.append(filename)
        return self.rank_results(result, string)

    def make_vectors(self, documents):
        vecs = {}
        for doc in documents:
            doc_vec = [0] * len(self.index.get_uniques())
            for ind, term in enumerate(self.index.get_uniques()):
                doc_vec[ind] = self.index.generate_score(term, doc)
            vecs[doc] = doc_vec
        return vecs

    def query_vec(self, query):
        pattern = re.compile('[\W_]+')
        query = pattern.sub(' ', query)
        queryls = query.split()
        query_vec = [0] * len(queryls)
        index = 0
        for ind, word in enumerate(queryls):
            query_vec[index] = self.query_freq(word, query)
            index += 1
        queryidf = [self.index.idf[word] for word in self.index.get_uniques()]
        magnitude = pow(sum(map(lambda x: x ** 2, query_vec)), .5)
        freq = self.termfreq(self.index.get_uniques(), query)
        # print('THIS IS THE FREQ')
        tf = [x / magnitude for x in freq]
        final = [tf[i] * queryidf[i] for i in range(len(self.index.get_uniques()))]
        # print(len([x for x in queryidf if x != 0]) - len(queryidf))
        return final

    @staticmethod
    def query_freq(term, query):
        count = 0
        # print(query)
        # print(query.split())
        for word in query.split():
            if word == term:
                count += 1
        return count

    def termfreq(self, terms, query):
        temp = [0] * len(terms)
        for i, term in enumerate(terms):
            temp[i] = self.query_freq(term, query)
        # print(self.query_freq(term, query))
        return temp

    @staticmethod
    def dot_product(doc1, doc2):
        if len(doc1) != len(doc2):
            return 0
        return sum([x * y for x, y in zip(doc1, doc2)])

    def rank_results(self, result_docs, query):
        vectors = self.make_vectors(result_docs)
        # print(vectors)
        query_vec = self.query_vec(query)
        # print(query_vec)
        results = [[self.dot_product(vectors[result], query_vec), result] for result in result_docs]
        # print(results)
        results.sort(key=lambda x: x[0])
        # print(results)
        results = [x[1] for x in results]
        return results

    def serve_query(self, string):
        string = str(string)
        # dskfjh askdjh | kljsdhf lsdkjfh | 'asldk asldkj'
        results = []
        for ele in string.split('|'):
            if '\'' not in ele:
                results.append(set(self.strict_text_query(ele)))
            else:
                results.append(set(self.phrase_query(ele.replace("'", ''))))
        results = list(set.union(*results))
        return results


"""Do this:
    Calculate a tf-idf score for every unique term in the collection, for each document. As in, find all unique terms, 
    and for each document, got through 
    each unique term and calculate a tf-idf score for it in the doc. You can do this already with the generate_score 
    function. Doc becomes array of scores.
    Calculate a tf-idf score for every unique term in the collection for the query.
    Find the cosine distance between each document and the query, and put the results in descending order.
"""
