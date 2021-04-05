from .util import *


class BoolSearch:
    def __init__(self):
        self.index = create_index()

    def get_index(self):
        return self.index

    def one_word_query(self, word):
        if word in self.index.keys():
            return [filename for filename in self.index[word].keys()]
        else:
            return []

    # 'OR' search
    def free_text_query(self, string):
        result = []
        for word in prepare_query(string):
            result += self.one_word_query(word)
        return list(set(result))

    # 'AND' search
    def strict_text_query(self, string):
        result = []
        for word in prepare_query(string):
            query = self.one_word_query(word)
            result = list(set(result) & set(query)) if result \
                else set(query)
        return result

    # 'PH' search
    def phrase_query(self, string):

        prepared_query = prepare_query(string)
        list_of_lists, result = [], []

        for word in prepared_query:
            list_of_lists.append(self.one_word_query(word))
        set_from_list = set(list_of_lists[0]).intersection(*list_of_lists)

        for filename in set_from_list:
            temp = []
            for word in prepared_query:
                temp.append(self.index[word][filename][:])
            for i in range(len(temp)):
                for ind in range(len(temp[i])):
                    temp[i][ind] -= i
            if set(temp[0]).intersection(*temp):
                result.append(filename)
        return [result, string]
