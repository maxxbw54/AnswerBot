# -*- coding: utf-8 -*-
import operator
import time
from utils.StopWords import remove_stopwords, read_EN_stopwords
from utils.db_util import read_all_questions_from_repo, read_specific_question_from_repo
import numpy as np
from utils.data_util import load_idf_vocab, load_w2v_model
from utils.csv_utils import write_list_to_csv
from utils.data_util import preprocessing_for_query
from pathConfig import res_dir
import os


def calc_wordvec_similarity(vec1, vec2):
    vec1 = vec1.reshape(1, len(vec1))
    vec2 = vec2.reshape(1, len(vec2))
    x1_norm = np.sqrt(np.sum(vec1 ** 2, axis=1, keepdims=True))
    x2_norm = np.sqrt(np.sum(vec2 ** 2, axis=1, keepdims=True))
    prod = np.sum(vec1 * vec2, axis=1, keepdims=True)
    cosine_sim = prod / (x1_norm * x2_norm)
    return cosine_sim[0][0]


def calc_similarity(word_list_1, word_list_2, idf_voc, word2vector_model):
    if len(word_list_1) == 0 or len(word_list_2) == 0:
        return 0.0

    sim_up = 0
    sim_down = 0
    for w1 in word_list_1:
        w1_unicode = w1.decode('utf-8')
        if w1_unicode in word2vector_model:
            w1_vec = word2vector_model[w1_unicode]
            # maxsim
            maxsim = 0.0
            for w2 in word_list_2:
                # word similarity
                w2_unicode = w2.decode('utf-8')
                if w2_unicode in word2vector_model:
                    w2_vec = word2vector_model[w2_unicode]
                    sim_tmp = calc_wordvec_similarity(w1_vec, w2_vec)
                    if sim_tmp > maxsim:
                        maxsim = sim_tmp
            # if exist in idf
            if w1 in idf_voc:
                idf = idf_voc[w1]
                sim_up += maxsim * idf
                sim_down += idf
            else:
                print("%s not in idf vocabulary!" % w1)
    if sim_down == 0:
        print("sim_down = 0!\n word sent 1 %s\nword sent 2 %s" % (word_list_1, word_list_2))
        return 0
    return sim_up / sim_down


def get_dq(query_w, topnum, repo):
    global idf_vocab, w2v_model
    rank = []
    stopwords = read_EN_stopwords()
    cnt = 0
    for q in repo:
        title_w = remove_stopwords(q.title, stopwords)
        sim = calc_similarity(query_w, title_w, idf_vocab, w2v_model)
        sim += calc_similarity(title_w, query_w, idf_vocab, w2v_model)
        sim /= 2.0
        rank.append([q.id, sim])
        cnt += 1
        if cnt % 10000 == 0:
            print("Processed %s questions." % cnt)

    # format: [id,sim]
    rank.sort(key=operator.itemgetter(1), reverse=True)
    # top_dq,rank
    top_dq = []
    for i in range(0, len(rank), 1):
        id = rank[i][0]
        sim = rank[i][1]
        rank.append(id)
        if i < topnum:
            q = read_specific_question_from_repo(id)
            top_dq.append((q, sim))
    return top_dq


# settings
topnum = 10
model_fpath = './_2_word2vec_model/model'
idf_vocab_fpath = './_3_IDF_vocabulary/idf_vocab.csv'

# load word2vec model
print 'load_textual_word2vec_model() : ', time.strftime('%Y-%m-%d %H:%M:%S')
w2v_model = load_w2v_model(model_fpath)
# load repo
print 'load repo :', time.strftime('%Y-%m-%d %H:%M:%S')
repo = read_all_questions_from_repo()
print 'load textual voc : ', time.strftime('%Y-%m-%d %H:%M:%S')
idf_vocab = load_idf_vocab(idf_vocab_fpath)

query_list = ["Differences between HashMap and Hashtable?"]
res = list()
for query in query_list:
    print("query : %s" % query)
    query_word = preprocessing_for_query(query)
    top_dq = get_dq(query_word, topnum, repo)
    cur_res_dict = []
    for i in range(len(top_dq)):
        q = top_dq[i][0]
        sim = top_dq[i][1]
        print "#%s\nId : %s\nTitle : %s\nSimilarity : %s\n" % (i, q.id, q.title, sim)
        cur_res_dict.append((q.id, round(sim, 2)))
    res.append([query, cur_res_dict])

res_fpath = os.path.join(res_dir, 'rq_res.csv')
header = ["query", "rq_id_list"]
write_list_to_csv(res, res_fpath, header)
