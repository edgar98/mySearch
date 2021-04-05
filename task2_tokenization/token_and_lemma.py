import os
import pickle
import re
import sys
from collections import Counter
from string import punctuation

from settings import *
import html2text
import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


def _tokenize_file(text):
    """
    Text to words list
    :param text: Input text
    :type text: str
    :return: Word list
    :rtype list
    """
    soup = BeautifulSoup(text, features="lxml")
    text = soup.get_text()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', str(text))
    text = re.sub(r'[-_]', ' ', str(text))
    return text.split()


def tokenize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', str(text))
    text = re.sub(r'[-_]', ' ', str(text))
    return text.split()


def get_words_from_dir(dir_name=TASK1_OUTPUT_PATH, save_to=TASK2_PATH, filename=WORDS_FILENAME, save=True):
    """
    Read words from every file in directory
    :param dir_name: directory to search files in
    :type dir_name: str
    :param save_to: save dir path
    :type save_to: str
    :param filename: Save file name
    :type filename: str
    :param save: Save file if True
    :type save: bool
    :return: list of words from files
    """
    try:
        if OVERRIDE_FILES:
            raise IOError
        with open(f"{save_to}{filename}") as f:
            print('File already exist. Reading from there')
            words = f.read().split()
        return words
    except IOError:
        # If not, read words from each file :)
        words = []  # list for words
        print(f'Reading words from files in {dir_name}')
        sentences = get_sentences_from_dir(dir_name)
        for sentence in sentences:
            words += tokenize_text(sentence[1])

        english_stopwords = stopwords.words("english")
        words = [word for word in words
                 if word not in english_stopwords
                 and word != " "
                 and word.strip() not in punctuation
                 and not len(word) <= 2]
        if save:
            _write_words_to_file(words, filename, save_to)
        return words


def _write_words_to_file(words, filename, save_to):
    """
    Write words to file
    :param words: List of words
    :type words: list
    :param filename: Save file name
    :type filename: str
    :param save_to: Save directory
    :type save_to: str
    :return: None
    """
    print(f'Writing words to {save_to}{filename}')
    with open(f'{save_to}{filename}', 'w', encoding=ENCODING) as file:
        for word in words:
            file.write(f'{word}\n')
    file.close()


def word_counter(tokens):
    word_counts = Counter()
    word_counts.update(tokens)
    return word_counts


def get_sentences_from_dir(dir_name=TASK1_OUTPUT_PATH, save_to=TASK2_PATH, _fname=SENTENCES_FILENAME, override=False):
    try:
        if override:
            raise IOError
        with open(f'{save_to}{_fname}', 'rb') as f1:
            sentences = pickle.load(f1)
            return sentences
    except IOError:
        sentences = []
        with os.scandir(dir_name) as files:
            for file in files:
                filename = file.path
                with open(filename, 'r', encoding=ENCODING) as f:
                    result = _tokenize(f.read(), filename)
                sentences.append(result)
        with open(f'{save_to}{_fname}', 'wb') as f2:
            pickle.dump(sentences, f2)
        return sentences


def _tokenize(text, filename):
    text = text.split(TEXT_BEFORE_TAG)[0]
    text = text.split(TEXT_AFTER_TAG)[1]
    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    text = h2t.handle(text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', str(text))
    text = re.sub(r'[-_]', ' ', str(text))
    text = text.split(CUT_FROM)[1:]
    text = ''.join([part.split(SPLIT_STR)[0] for part in text]).strip()
    res = [filename, text]
    return res


def get_lemmas(words, save_to='', save=True, filename=TOKENS_FILENAME):
    words_count = word_counter(words)
    nlp = spacy.load(SPACY_CORE)

    tokens = {}
    total_words = len(list(words_count))
    for idx, word in enumerate(list(words_count)):
        sys.stdout.write(f'\rWord {idx}/{total_words} {"%.1f" % (idx/total_words * 100)}%')
        sys.stdout.flush()
        doc = nlp(word)
        for token in doc:
            if token.lemma_ in tokens:
                tokens[token.lemma_].append(token.text)
            else:
                tokens[token.lemma_] = []
                tokens[token.lemma_].append(token.text)
    sys.stdout.write(" - DONE\n")
    sys.stdout.flush()
    if save:
        sys.stdout.write("SAVING")
        sys.stdout.flush()
        with open(f'{save_to}{filename}', 'w', encoding=ENCODING) as file:
            for key, words_tokens in tokens.items():
                file.write(f'{key} ')
                for word in words_tokens:
                    file.write(f'{word} ')
                file.write('\n')
        sys.stdout.write(' - DONE')
        sys.stdout.flush()
    return tokens


def get_tokens(filename=TASK2_PATH + TOKENS_FILENAME, encoding=ENCODING):
    tokens = {}
    with open(filename, 'r', encoding=encoding) as tokens_file:
        for line in tokens_file:
            parts = line.split()
            tokens[parts[0]] = parts[1:]
    return tokens
