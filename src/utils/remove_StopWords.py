# -*- coding: UTF-8 -*-
from pathutil import get_base_path

path_of_stopwords_EN = get_base_path() + '/utils/StopWords_EN.txt'


def read_EN_stopwords():
    stopword_list = []
    f = open(path_of_stopwords_EN)
    for line in f:
        stopword_list.append(line.strip())
    return stopword_list


def remove_stopwords(wordlist, stopwords):
    new_wordlist = []
    for word in wordlist:
        word = word.strip()
        if word == '':
            continue
        if word not in stopwords:
            new_wordlist.append(word)
    return new_wordlist
