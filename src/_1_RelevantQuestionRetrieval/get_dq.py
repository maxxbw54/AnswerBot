# -*- coding: utf-8 -*-
import operator
from util.data_util import preprocessing_for_general_text
from _1_RelevantQuestionRetrieval.Textual.textual_util import load_textual_word2vec_model, read_Textual_IDF_voc
from _1_RelevantQuestionRetrieval.Textual.textual_util import calc_wordembedding_similarity_by_textual
import time
from util.remove_StopWords import remove_stopwords, read_EN_stopwords
import sys
from pathutil import get_base_path
from util.experiment_util import save_dq_result_baseline
from data.dataset_util import read_query_for_testing
from util.db_util import read_all_questions_from_repo, read_specific_question_from_repo


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
        textual_similarity = calc_wordembedding_similarity_by_textual(query_word, SO_dataUnit.title_NO_SW,
                                                                      size_of_textual_repo, textual_IDF_voc,
                                                                      textual_word2vec_model)
        textual_similarity += calc_wordembedding_similarity_by_textual(SO_dataUnit.title_NO_SW, query_word,
                                                                       size_of_textual_repo, textual_IDF_voc,
                                                                       textual_word2vec_model)
        textual_similarity /= 2.0
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
    # remove itself
    ranklist.remove(ranklist[0])
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
    # [query_id, query, relevant id]
    query_list = read_query_for_testing()
    # parameter
    topnum = 10
    approach_name = 'myapproach'
    dir_of_result = get_base_path() + '/_1_Result/Baseline_' + approach_name + '/'
    size_of_textual_repo = 228917
    # load word2vec model
    print 'load_textual_word2vec_model() : ', time.strftime('%Y-%m-%d %H:%M:%S')
    textual_word2vec_model = load_textual_word2vec_model()
    # load repo
    print 'load repo :', time.strftime('%Y-%m-%d %H:%M:%S')
    repo = read_all_questions_from_repo()
    print 'load textual voc : ', time.strftime('%Y-%m-%d %H:%M:%S')
    textual_IDF_voc = read_Textual_IDF_voc()

    result = []
    for i in range(0, len(query_list), 1):
        print 'processing No.' + str(i + 1) + ' query', time.strftime('%Y-%m-%d %H:%M:%S')
        query_id = query_list[i][0]
        query = query_list[i][1].strip()
        high_relevant_id = query_list[i][2]
        top_dq, rank = get_dq(query, topnum, repo, size_of_textual_repo, textual_IDF_voc, textual_word2vec_model)
        result.append([high_relevant_id, rank])
        save_dq_result_baseline(i, query, top_dq, dir_of_result + str(i), high_relevant_id, rank)
    print 'Done.'
