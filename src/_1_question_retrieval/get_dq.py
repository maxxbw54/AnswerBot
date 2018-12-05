# -*- coding: utf-8 -*-
import operator
from _1_question_retrieval.utils1 import load_w2v_model, load_idf_voccab
import time
from utils.StopWords import remove_stopwords, read_EN_stopwords
from utils.db_util import read_all_questions_from_repo, read_specific_question_from_repo
from nltk import word_tokenize
import numpy as np
import math


def preprocessing_for_query(q):
    # basic preprocessing for query
    qw = word_tokenize(q.lower())
    stopwords = read_EN_stopwords()
    qw = remove_stopwords(qw, stopwords)
    return qw


def calc_wordvec_similarity(vec1, vec2):
    vec1 = vec1.reshape(1, len(vec1))
    vec2 = vec2.reshape(1, len(vec2))
    x1_norm = np.sqrt(np.sum(vec1 ** 2, axis=1, keepdims=True))
    x2_norm = np.sqrt(np.sum(vec2 ** 2, axis=1, keepdims=True))
    prod = np.sum(vec1 * vec2, axis=1, keepdims=True)
    cosine_sim = prod / (x1_norm * x2_norm)
    return cosine_sim[0][0]


def calc_similarity(query_word, title_NO_SW, size_of_repo, textual_IDF_voc, word2vector_model):
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
    # (include_num / len_doc) to differ 'code review tool' and 'use code review tool'
    if sim_down == 0:
        return 0
    else :
        sim = sim_up / sim_down
        return sim


def get_dq(query_w, topnum, repo):
    global idf_vocab, w2v_model
    repo_size = len(repo)
    rank = []
    stopwords = read_EN_stopwords()
    for q in repo:
        title_w = remove_stopwords(q.title, stopwords)
        textual_similarity = calc_similarity(query_w, title_w, repo_size, idf_vocab, w2v_model)
        textual_similarity += calc_similarity(title_w, query_w, repo_size, idf_vocab, w2v_model)
        textual_similarity /= 2.0
        rank.append([q.id, textual_similarity])

    # format: [id,sim]
    rank.sort(key=operator.itemgetter(1), reverse=True)
    # top_dq,rank
    rank = []
    top_dq = []
    for i in range(0, len(rank), 1):
        id = rank[i][0]
        sim = rank[i][1]
        rank.append(id)
        if i < topnum:
            q = read_specific_question_from_repo(id)
            top_dq.append([q, sim])
    return top_dq, rank


# settings
topnum = 10

# load word2vec model
print 'load_textual_word2vec_model() : ', time.strftime('%Y-%m-%d %H:%M:%S')
w2v_model = load_w2v_model()
# load repo
print 'load repo :', time.strftime('%Y-%m-%d %H:%M:%S')
repo = read_all_questions_from_repo()
print 'load textual voc : ', time.strftime('%Y-%m-%d %H:%M:%S')
idf_vocab = load_idf_voccab()

query = ""
query_word = preprocessing_for_query(query)
top_dq = get_dq(query_word, topnum, repo)
for i in range(len(top_dq)):
    q = top_dq[i][0]
    sim = top_dq[i][1]
    print "#%s\nId : %s\nTitle : %s\nSimilarity : %s\n" % (i, q.id, q.title, sim)
print 'Done.'
