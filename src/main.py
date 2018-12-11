import os
import time

from _1_question_retrieval.get_dq import get_dq
from _2_sentence_selection.get_ss import get_ss
from _3_summarization.get_summary import get_summary
from pathConfig import res_dir
from utils.csv_utils import write_list_to_csv
from utils.data_util import load_idf_vocab, load_w2v_model
from utils.data_util import preprocessing_for_query
from utils.db_util import read_all_questions_from_repo

if __name__ == '__main__':
    topnum = 10
    # load word2vec model
    print 'load_textual_word2vec_model() : ', time.strftime('%Y-%m-%d %H:%M:%S')
    w2v_model = load_w2v_model()
    # load repo
    print 'load repo :', time.strftime('%Y-%m-%d %H:%M:%S')
    repo = read_all_questions_from_repo()
    # load idf
    print 'load textual voc : ', time.strftime('%Y-%m-%d %H:%M:%S')
    idf_vocab = load_idf_vocab()

    query_list = ["Differences between HashMap and Hashtable?"]
    dq_res = list()
    for query in query_list:
        print("query : %s" % query)
        query_word = preprocessing_for_query(query)
        top_dq = get_dq(query_word, topnum, repo, idf_vocab, w2v_model)
        cur_res_dict = []
        for i in range(len(top_dq)):
            q = top_dq[i][0]
            sim = top_dq[i][1]
            # print "#%s\nId : %s\nTitle : %s\nSimilarity : %s\n" % (i, q.id, q.title, sim)
            cur_res_dict.append((q.id, round(sim, 2)))
        dq_res.append([query, cur_res_dict])

    dqres_fpath = os.path.join(res_dir, 'rq_res.csv')
    header = ["query", "rq_id_list"]
    write_list_to_csv(dq_res, dqres_fpath, header)

    print 'sentence selection...', time.strftime('%Y-%m-%d %H:%M:%S')
    ss_res = list()
    for query, top_dq_id_and_sim in dq_res:
        top_ss = get_ss(query, topnum, top_dq_id_and_sim)
        ss_res.append((query, top_ss))
    print 'get summary...', time.strftime('%Y-%m-%d %H:%M:%S')
    res = list()
    for query, ss in ss_res:
        query = ' '.join(preprocessing_for_query(query))
        sum = get_summary(query, ss, 5)
        res.append([query, sum])

    res_fpath = os.path.join(res_dir, 'summary_res.csv')
    header = ["query", "summary"]
    write_list_to_csv(res, res_fpath, header)

