import pickle
import sys
import spacy

from settings import *
from nltk.corpus import stopwords
from task2_tokenization import token_and_lemma


def create_index(override=OVERRIDE_FILES):
    index = {}
    try:
        if override:
            raise IOError
        with open(TASK3_PATH + INVERTED_FILENAME, 'rb') as file:
            index = pickle.load(file)
            return index

    except IOError:

        sentences = token_and_lemma.get_sentences_from_dir(TASK1_OUTPUT_PATH)
        tokens = token_and_lemma.get_tokens(TASK2_PATH + TOKENS_FILENAME)
        len_sent = len(sentences)
        english_stopwords = stopwords.words("english")

        for idx, sentence in enumerate(sentences):

            sys.stdout.write(f'\rsentence {idx + 1} of {len_sent}')
            sys.stdout.flush()

            sentence_split = sentence[1].split()

            for word_idx, word in enumerate(sentence_split):  # for word in sentence, word_idx is word position
                if word in english_stopwords:
                    continue
                for lemma, tokens_of_lemma in tokens.items():  # k is lemma, v is tokens
                    if word in tokens_of_lemma:  # if word in tokens value
                        if lemma not in index:
                            index[lemma] = {sentence[0]: [word_idx]}
                            break
                        else:
                            if sentence[0] not in index[lemma]:
                                index[lemma][sentence[0]] = [word_idx]
                            else:
                                index[lemma][sentence[0]].append(word_idx)
                            break
        with open(TASK3_PATH + INVERTED_FILENAME, 'wb') as f2:
            pickle.dump(index, f2)
        del len_sent, idx, sentence
        sys.stdout.write('\n')
        sys.stdout.flush()
        return index


def save_result():
    pass


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
