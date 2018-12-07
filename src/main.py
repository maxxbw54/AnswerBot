# -*- coding: UTF-8 -*-

import time
import operator
from pathConfig import get_base_path
from _3_summarization.MMR_Analysis import MMR_Analysis
from utils.data_util import load_idf_vocab, load_w2v_model
from utils.db_util import read_all_questions_from_repo
from _1_question_retrieval.get_dq import get_dq
from _2_sentence_selection import get_ss

if __name__ == '__main__':
    print 'start : ', time.strftime('%Y-%m-%d %H:%M:%S')

    # setting
    query = 'what are the Differences between HashMap and Hashtable'
    # load word2vec model
    print 'load_textual_word2vec_model() : ', time.strftime('%Y-%m-%d %H:%M:%S')
    textual_word2vec_model = load_w2v_model()
    # load repo
    print 'load repo :', time.strftime('%Y-%m-%d %H:%M:%S')
    repo = read_all_questions_from_repo()
    print 'load textual voc : ', time.strftime('%Y-%m-%d %H:%M:%S')
    textual_IDF_voc = load_idf_vocab()

    #  get Step.1 get relevant questions [query -> top_dq]
    top_relevant_question_num = 5
    dir_of_result = get_base_path() + '/_1_Result/Baseline_Only_Text/'
    top_dq, rank = get_dq(query, top_relevant_question_num, repo, textual_IDF_voc, textual_word2vec_model)
    # get step.2
    # parameter
    top_relevant_paragraph_num = 5
    # Step 2. select relevant sentences based on
    # print 'get relevant sentence', time.strftime('%Y-%m-%d %H:%M:%S')
    # return format : [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id]
    top_ss = get_ss(query, top_relevant_paragraph_num + 5, top_dq)
    selected_sentence = MMR_Analysis(query, top_ss, top_relevant_paragraph_num)
    # sort by q_id then order
    selected_sentence.sort(key=operator.itemgetter(5, 3), reverse=True)
    print 'Summary : '
    for [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id] in selected_sentence:
        print raw_sent.strip()
    print 'Done. ', time.strftime('%Y-%m-%d %H:%M:%S')
