import pickle

import task2_tokenization.token_and_lemma as token
from task3_index.index_search import BoolSearch
from task4_tf_idf.tf_idf import TfIdfIndex

RUN_TASKS = [
    # 2,
    # 3,
    # 4,
    5,
]

if __name__ == '__main__':

    if 2 in RUN_TASKS:

        '''                               TASK 2                              '''
        words = token.get_words_from_dir()
        lemmas = token.get_lemmas(words)
    if 3 in RUN_TASKS:

        '''                               TASK 3                              '''
        bs = BoolSearch()

        print(bs.free_text_query('apollo apollo'))
        print(bs.strict_text_query('taking time'))
        print(bs.phrase_query('taking time'))

    if 4 in RUN_TASKS:

        '''                               TASK 4                              '''
        try:
            with open('task4_tf_idf/entity.bin', 'rb') as file:
                index = pickle.load(file)
        except IOError:
            index = TfIdfIndex()
            with open('task4_tf_idf/entity.bin', 'wb') as file:
                pickle.dump(index, file)
    if 5 in RUN_TASKS:
        pass
