# -*- coding: UTF-8 -*-

from _3_summarization.MMR_Analysis import MMR_Analysis
from _2_sentence_selection import get_ss
from utils.file_util import write_file
import operator
from utils.preprocessing_util import preprocessing_for_general_text
from utils.data_util import load_idf_vocab, load_w2v_model
from _1_question_retrieval.Textual.textual_util import calc_wordembedding_similarity_by_textual
import time
from utils.StopWords import remove_stopwords, read_EN_stopwords
import sys
from pathConfig import get_base_path
from data.dataset_util import read_query_for_testing
from utils.db_util import read_all_questions_from_repo, read_specific_question_from_repo


def get_dq(query, topnum, repo, size_of_textual_repo, textual_IDF_voc, textual_word2vec_model):
    max_Textual = -sys.float_info.max
    min_Textual = sys.float_info.max
    query = query.lower()
    query_textual = preprocessing_for_general_text(query)
    # textual, no need for stemming
    stopwords = read_EN_stopwords()
    query_word = remove_stopwords(query_textual.split(' '), stopwords)
    dq_list = []
    # count = 0
    for SO_dataUnit in repo:
        # if count % 30000 == 0:
        #     print 'processing ' + str(count) + ' Unit  ' + time.strftime('%Y-%m-%d %H:%M:%S')
        # count += 1
        # print 'calc textual sim : ', time.strftime('%Y-%m-%d %H:%M:%S')
        textual_similarity = calc_wordembedding_similarity_by_textual(query_word, SO_dataUnit.title_NO_SW,
                                                                      size_of_textual_repo, textual_IDF_voc,
                                                                      textual_word2vec_model)
        # textual
        max_Textual = textual_similarity if max_Textual < textual_similarity else max_Textual
        min_Textual = textual_similarity if min_Textual > textual_similarity else min_Textual
        dq_list.append(
            [SO_dataUnit.id, textual_similarity])
    # Normalization
    # print 'Normalization : ', time.strftime('%Y-%m-%d %H:%M:%S')
    ranklist = []
    for [id, textual_similarity] in dq_list:
        textual_similarity = 0.0 if (max_Textual - min_Textual) == 0 else (textual_similarity - min_Textual) / (
            max_Textual - min_Textual)
        ranklist.append([id, textual_similarity])
    # format: [id,sim]
    ranklist.sort(key=operator.itemgetter(1), reverse=True)
    # top_dq,rank
    rank = []
    top_dq = []
    for i in range(0, len(ranklist), 1):
        id = ranklist[i][0]
        sim = ranklist[i][1]
        rank.append(id)
        if i < topnum:
            title = read_specific_question_from_repo(id).title
            top_dq.append([id, title, sim])
    return top_dq, rank


if __name__ == '__main__':
    print 'start : ', time.strftime('%Y-%m-%d %H:%M:%S')
    # [query_id, query, relevant id]
    query_list = read_query_for_testing()
    #  get Step.1 result [query -> top_dq]
    # parameter
    top_relevant_question_num = 5
    dir_of_result = get_base_path() + '/_1_Result/Baseline_Only_Text/'
    size_of_textual_repo = 228917
    # load word2vec model
    print 'load_textual_word2vec_model() : ', time.strftime('%Y-%m-%d %H:%M:%S')
    textual_word2vec_model = load_w2v_model()
    # load repo
    print 'load repo :', time.strftime('%Y-%m-%d %H:%M:%S')
    repo = read_all_questions_from_repo()
    print 'load textual voc : ', time.strftime('%Y-%m-%d %H:%M:%S')
    textual_IDF_voc = load_idf_vocab()

    for i in range(0, len(query_list)):
        print 'precessing ' + str(i), time.strftime('%Y-%m-%d %H:%M:%S')
        query = query_list[i][1]
        write_str = 'query : ' + query + '\n'
        top_dq, rank = get_dq(query, top_relevant_question_num, repo, size_of_textual_repo, textual_IDF_voc,
                              textual_word2vec_model)
        for [id, title, sim] in top_dq:
            write_str += ('relevant question title : ' + title + '\n')
        # get step.2 result
        # parameter
        top_relevant_paragraph_num = 5
        # Step 2. select relevant sentences based on
        # print 'get relevant sentence', time.strftime('%Y-%m-%d %H:%M:%S')
        # return format : [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id]
        top_ss = get_ss(query, top_relevant_paragraph_num + 5, top_dq)
        selected_sentence = MMR_Analysis(query, top_ss, top_relevant_paragraph_num)
        # sort by q_id then order
        selected_sentence.sort(key=operator.itemgetter(5, 3), reverse=True)
        write_str += ('\nSummary :\n')
        for [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id] in selected_sentence:
            write_str += (raw_sent.strip() + '\n')
        write_file(get_base_path() + '/summary_include_itself/' + str(i) + '.txt', write_str)
    print 'Done. ', time.strftime('%Y-%m-%d %H:%M:%S')
