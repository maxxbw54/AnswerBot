# -*- coding: utf-8 -*-
import gensim
from utils.db_util import read_questions_from_repo
from pathutil import get_base_path
from utils.Stemming import stemming
import numpy as np
import math

path_of_model = get_base_path() + '/_1_RelevantQuestionRetrieval/_2_Word2vecModel/model'


def load_textual_word2vec_model():
    word2vector_model = gensim.models.Word2Vec.load(path_of_model)
    return word2vector_model


def load_textual_repo(num):
    repo = read_questions_from_repo(num)
    return repo


def calc_wordvec_similarity(vec1, vec2):
    vec1 = vec1.reshape(1, len(vec1))
    vec2 = vec2.reshape(1, len(vec2))
    x1_norm = np.sqrt(np.sum(vec1 ** 2, axis=1, keepdims=True))
    x2_norm = np.sqrt(np.sum(vec2 ** 2, axis=1, keepdims=True))
    prod = np.sum(vec1 * vec2, axis=1, keepdims=True)
    cosine_sim = prod / (x1_norm * x2_norm)
    return cosine_sim[0][0]


def calc_wordembedding_similarity_by_textual(query_word, title_NO_SW, size_of_repo, textual_IDF_voc, word2vector_model):
    title_word = title_NO_SW.split(' ')
    len_doc = len(title_word)
    if len_doc == 0:
        return 0.0

    sim_up = 0
    sim_down = 0
    for q_word in query_word:
        q_word_unicode = q_word.decode('utf-8')
        if q_word_unicode in word2vector_model:
            q_wordvec = word2vector_model[q_word_unicode]
            # maxsim
            maxsim = 0.0
            for t_word in title_word:
                # word similarity
                t_word_unicode = t_word.decode('utf-8')
                if t_word_unicode in word2vector_model:
                    t_wordvec = word2vector_model[t_word_unicode]
                    sim_tmp = calc_wordvec_similarity(q_wordvec, t_wordvec)
                    if sim_tmp > maxsim:
                        maxsim = sim_tmp
            # idf
            idf = math.log(float(size_of_repo))
            if q_word in textual_IDF_voc:
                idf = textual_IDF_voc[q_word]
            sim_up += maxsim * idf
            sim_down += idf
    sim = sim_up / sim_down
    return sim


def read_Textual_IDF_voc():
    path = get_base_path() + '/_1_RelevantQuestionRetrieval/_3_IDF_vocabulary/idf_voc.txt'
    file = open(path)
    voc = {}
    for line in file:
        line = line.strip().split(' ')
        voc[line[0]] = float(line[1])
    return voc
