# -*- coding: UTF-8 -*-
from util.data_util import replace_double_space
from util.Stemming import stemming_for_word_list
from util.remove_StopWords import remove_stopwords
from build_tf_idf_dic import remove_duplicate_element
from build_tf_idf_dic import read_voc


# remove the stopwords and query words from the sentence, then calculate the entropy of the rest.
# calculate the meaning tf-idf of the rest word as the entropy
def get_entropy_score(query_words, title, stopwords):
    # preprocessing for title, lower
    title = title.replace('. ', ' ').replace('? ', ' ').replace('! ', ' ').strip().lower()
    title = replace_double_space(title)
    title_words = title.split(' ')
    # remove stopwords
    title_words = remove_stopwords(title_words, stopwords)
    # remove duplicate word in list
    query_words = remove_duplicate_element(query_words)
    title_words = remove_duplicate_element(title_words)
    # stemming
    query_words = stemming_for_word_list(query_words)
    title_words = stemming_for_word_list(title_words)
    # remove query word
    for word in query_words:
        if word in title_words:
            title_words.remove(word)
    voc = read_voc()
    entropy = 0.0
    for word in title_words:
        if word in voc.keys():
            entropy += float(voc[word])
    return entropy
