# -*- coding: UTF-8 -*-
from pathConfig import get_base_path
from nltk import tokenize

path_of_stopwords_EN = get_base_path() + '/utils/StopWords_EN.txt'


def read_EN_stopwords():
    sw_set = set()
    f = open(path_of_stopwords_EN)
    for line in f:
        sw_set.add(line.strip())
    return sw_set


def remove_stopwords(sent, sw):
    wlist = sent
    new_sent = ''
    for w in wlist:
        if w == '':
            continue
        if w not in sw:
            new_sent += (' ' + w)
    return new_sent.strip()
