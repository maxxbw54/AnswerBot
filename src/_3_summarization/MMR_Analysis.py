# -*- coding: UTF-8 -*-

from utils.StopWords import read_EN_stopwords
import sys
import copy
import math
import numpy as np
from _1_question_retrieval.utils1 import load_w2v_model, load_idf_voccab
from utils.StopWords import remove_stopwords
from utils.data_util import replace_double_space


def calc_wordvec_similarity(vec1, vec2):
    vec1 = vec1.reshape(1, len(vec1))
    vec2 = vec2.reshape(1, len(vec2))
    x1_norm = np.sqrt(np.sum(vec1 ** 2, axis=1, keepdims=True))
    x2_norm = np.sqrt(np.sum(vec2 ** 2, axis=1, keepdims=True))
    prod = np.sum(vec1 * vec2, axis=1, keepdims=True)
    cosine_sim = prod / (x1_norm * x2_norm)
    return cosine_sim[0][0]


def calc_similarity_by_wordembedding(wordlist1, wordlist2, textual_IDF_voc, word2vector_model):
    size_of_repo = 228917
    len_1 = len(wordlist1)
    len_2 = len(wordlist2)
    if len_1 == 0 or len_2 == 0:
        return 0.0

    sim_up = 0
    sim_down = 0
    for word_1 in wordlist1:
        word_1_unicode = word_1.decode('utf-8')
        # maxsim
        maxsim = 0.0
        if word_1_unicode in word2vector_model:
            wordvec_1 = word2vector_model[word_1_unicode]
            for word_2 in wordlist2:
                # word similarity
                word_2_unicode = word_2.decode('utf-8')
                if word_2_unicode in word2vector_model:
                    wordvec_2 = word2vector_model[word_2_unicode]
                    sim_tmp = calc_wordvec_similarity(wordvec_1, wordvec_2)
                    if sim_tmp > maxsim:
                        maxsim = sim_tmp
        # idf
        idf = math.log(float(size_of_repo))
        if word_1 in textual_IDF_voc:
            idf = textual_IDF_voc[word_1]
        sim_up += maxsim * idf
        sim_down += idf
    # (include_num / len_doc) to differ 'code review tool' and 'use code review tool'
    sim = sim_up / sim_down
    return sim


# top_ss format: [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id]

def MMR_Analysis(query, top_ss, topnum):
    # print 'MMR analysis', time.strftime('%Y-%m-%d %H:%M:%S')
    sim_matrix = build_sim_matrix(query, top_ss)
    rank_list = MMR_Algorithm(sim_matrix, topnum)
    selected_sentence = []
    for rank in rank_list:
        selected_sentence.append(top_ss[rank])
    return selected_sentence


######### Matrix #########
#      d1 d2 ... dn query
# d1   1  S1,2  S1,n
# d2      1
# ...        ...
# dn             1
# query              1
##########################

'''
top_ss format : [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id]
'''


def build_sim_matrix(query, top_ss):
    # add query
    top_ss_tmp = copy.deepcopy(top_ss)
    top_ss_tmp.append(['-1', query, query])
    len_of_paragraph = len(top_ss_tmp)
    sim_matrix = [[0 for col in range(len_of_paragraph)] for row in range(len_of_paragraph)]
    # doc sim parameter
    word_embedding_model = load_w2v_model()
    stopwords = read_EN_stopwords()
    textual_IDF_voc = load_idf_voccab()
    for i in range(0, len_of_paragraph, 1):
        text_i_wordlist = replace_double_space(top_ss_tmp[i][2].replace('.', ' ').replace('/', ' ')).split(' ')
        text_i_wordlist = remove_stopwords(text_i_wordlist, stopwords)
        for j in range(0, i + 1, 1):
            if i == j:
                sim_matrix[i][j] = 1.0
            elif i == (len_of_paragraph - 1):
                # sim(d,query) = Score
                sim_matrix[i][j] = top_ss_tmp[j][4]
                sim_matrix[j][i] = sim_matrix[i][j]
            else:
                text_j_wordlist = replace_double_space(top_ss_tmp[j][2].replace('.', ' ').replace('/', ' ')).split(' ')
                text_j_wordlist = remove_stopwords(text_j_wordlist, stopwords)
                sim_matrix[i][j] = (calc_similarity_by_wordembedding(text_i_wordlist, text_i_wordlist, textual_IDF_voc,
                                                                     word_embedding_model) +
                                    calc_similarity_by_wordembedding(text_j_wordlist, text_i_wordlist, textual_IDF_voc,
                                                                     word_embedding_model)) / 2.0
                sim_matrix[j][i] = sim_matrix[i][j]
    return sim_matrix


def MMR_Algorithm(sim_matrix, topnum):
    iteration = 1
    query_index = len(sim_matrix) - 1
    # init
    Set = []
    Rest = [i for i in range(0, query_index - 1, 1)]
    # parameter
    Lambda = 0.5
    while iteration <= topnum:
        # find most sim with query
        most_sim_with_query_index = -1
        max_dq_sim = -1
        for i in range(0, query_index, 1):
            if sim_matrix[i][query_index] > max_dq_sim:
                max_dq_sim = sim_matrix[i][query_index]
                most_sim_with_query_index = i
        if len(Set) == 0:
            Set.append(most_sim_with_query_index)
            Rest.remove(most_sim_with_query_index)
        else:
            max_MMR = -sys.float_info.max
            max_MMR_idx = -1
            for cur in Rest:
                max_dd_sim = -sys.float_info.max
                max_dd_idx = -1
                for i in Set:
                    if sim_matrix[cur][i] > max_dd_sim:
                        max_dd_sim = sim_matrix[cur][i]
                        max_dd_idx = i
                MRR_tmp = Lambda * sim_matrix[cur][query_index] - (1 - Lambda) * sim_matrix[cur][max_dd_idx]
                if MRR_tmp > max_MMR:
                    max_MMR = MRR_tmp
                    max_MMR_idx = cur
            Set.append(max_MMR_idx)
            Rest.remove(max_MMR_idx)
        iteration += 1
    return Set


######## Test Matrix #########
# [1,0.11,0.23,0.76,0.25,0.91]
# [0.11,1,0.29,0.57,0.51,0.90]
# [0.23,0.29,1,0.02,0.20,0.50]
# [0.76,0.57,0.02,1,0.33,0.06]
# [0.25,0.51,0.20,0.33,1,0.63]
# [0.91,0.90,0.50,0.06,0.63,1]
##############################


if __name__ == '__main__':
    sim_matrix = [[1, 0.11, 0.23, 0.76, 0.25, 0.91], [0.11, 1, 0.29, 0.57, 0.51, 0.90],
                  [0.23, 0.29, 1, 0.02, 0.20, 0.50], [0.76, 0.57, 0.02, 1, 0.33, 0.06],
                  [0.25, 0.51, 0.20, 0.33, 1, 0.63], [0.91, 0.90, 0.50, 0.06, 0.63, 1]]
    topnum = 3
    Set = MMR_Algorithm(sim_matrix, topnum)
    print Set
