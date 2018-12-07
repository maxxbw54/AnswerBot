# -*- coding: UTF-8 -*-

from utils.db_util import read_correspond_answer_from_java_table
from utils.str_util import split_into_paragraph
import time
import operator
from _2_sentence_selection.Order.Order_Analysis import get_order_score
from _2_sentence_selection.Pattern.Pattern_Analysis import get_pattern_score
from _2_sentence_selection.HTMLTag.HTML_Analysis import get_html_score
from _2_sentence_selection.Entropy.Entropy_Analysis import get_entropy_score
from _2_sentence_selection.Entity.Entity_Analysis import get_entity_score, get_entities_from_text
from utils.StopWords import read_EN_stopwords, remove_stopwords
import sys
from utils.preprocessing_util import replace_double_space
from pathConfig import res_dir
import os
from utils.data_util import preprocessing_for_query

'''
return format : [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id]
'''


def get_ss(query, top_relevant_paragraph_num, top_dq_id_list):
    sent_list = []
    # Relevance
    max_Relevance = -sys.float_info.max
    min_Relevance = sys.float_info.max
    # Entity
    max_Entity = -sys.float_info.max
    min_Entity = sys.float_info.max
    # Score
    max_A_Score = -sys.float_info.max
    min_A_Score = sys.float_info.max
    # Order
    max_Order = -sys.float_info.max
    min_Order = sys.float_info.max
    # Pattern
    max_Pattern = -sys.float_info.max
    min_Pattern = sys.float_info.max
    # HTMLTag
    max_HTMLTag = -sys.float_info.max
    min_HTMLTag = sys.float_info.max
    # Entropy
    max_Entropy = -sys.float_info.max
    min_Entropy = sys.float_info.max
    # Score
    max_Score = -sys.float_info.max
    min_Score = sys.float_info.max

    # For Entropy calculation : preprocessing for query
    query_words = preprocessing_for_query(query)
    # query entities
    query_entities = get_entities_from_text(query)

    # question-level
    sent_Num = 0
    for [q_id, title, sim] in top_dq_id:
        answers = read_correspond_answer_from_java_table(q_id)
        # answer-level
        for answer_tmp in answers:
            answer_desc = answer_tmp.desc
            # plus 0.1 to avoid zero score
            answer_score = (answer_tmp.score + 0.1)
            sentences = split_into_paragraph(answer_desc)
            order = 1
            # paragraph-level
            for sent in sentences:
                sent_without_tag = sent.replace('<strong>', ' ').replace('</strong>', ' ').replace('<code>',
                                                                                                   ' ').replace(
                    '</code>', ' ').replace('<strike>', ' ').replace('</strike>', ' ').replace('.', ' ').replace('/',
                                                                                                                 ' ').lower()
                sent_without_tag = replace_double_space(sent_without_tag)
                # relevance
                Relevance = sim
                max_Relevance = Relevance if max_Relevance < Relevance else max_Relevance
                min_Relevance = Relevance if min_Relevance > Relevance else min_Relevance
                # entity
                Entity = get_entity_score(query_entities, sent_without_tag)
                max_Entity = Entity if max_Entity < Entity else max_Entity
                min_Entity = Entity if min_Entity > Entity else min_Entity
                # score
                A_Score = answer_score
                max_A_Score = A_Score if max_A_Score < A_Score else max_A_Score
                min_A_Score = A_Score if min_A_Score > A_Score else min_A_Score
                # Order
                Order = get_order_score(order)
                order += 1
                max_Order = Order if max_Order < Order else max_Order
                min_Order = Order if min_Order > Order else min_Order
                # Pattern
                Pattern = get_pattern_score(sent_without_tag)
                max_Pattern = Pattern if max_Pattern < Pattern else max_Pattern
                min_Pattern = Pattern if min_Pattern > Pattern else min_Pattern
                # HTML Tag
                HTMLTag = get_html_score(sent)
                max_HTMLTag = HTMLTag if max_HTMLTag < HTMLTag else max_HTMLTag
                min_HTMLTag = HTMLTag if min_HTMLTag > HTMLTag else min_HTMLTag
                # Entropy
                Entropy = get_entropy_score(query_words, sent_without_tag, stopwords)
                max_Entropy = Entropy if max_Entropy < Entropy else max_Entropy
                min_Entropy = Entropy if min_Entropy > Entropy else min_Entropy
                # set final score
                Score = 0.0
                # add
                raw_sent = sent.replace('<strong>', ' ').replace('</strong>', ' ').replace('<code>', ' ').replace(
                    '</code>', ' ').replace('<strike>', ' ').replace('</strike>', ' ')
                sent_list.append(
                    [sent_Num, raw_sent, sent_without_tag, Relevance, Entity, A_Score, Order, Pattern, HTMLTag, Entropy,
                     Score, q_id])
                sent_Num += 1
    # print 'sort [sentence,score]', time.strftime('%Y-%m-%d %H:%M:%S')

    # Normalization from 1.0 -> 2.0 except Score
    Normalized_sent_list_tmp = []
    for [sent_Num, raw_sent, sent_without_tag, Relevance, Entity, A_Score, Order, Pattern, HTMLTag, Entropy, Score,
         q_id] in sent_list:
        Relevance = 1.0 if (max_Relevance - min_Relevance) == 0 else 1.0 + (Relevance - min_Relevance) / (
                max_Relevance - min_Relevance)
        Entity = 1.0 if (max_Entity - min_Entity) == 0 else 1.0 + (Entity - min_Entity) / (max_Entity - min_Entity)
        A_Score = 1.0 if (max_A_Score - min_A_Score) == 0 else 1.0 + (A_Score - min_A_Score) / (
                max_A_Score - min_A_Score)
        Order = 1.0 if (max_Order - min_Order) == 0 else 1.0 + (Order - min_Order) / (max_Order - min_Order)
        Pattern = 1.0 if (max_Pattern - min_Pattern) == 0 else 1.0 + (Pattern - min_Pattern) / (
                max_Pattern - min_Pattern)
        HTMLTag = 1.0 if (max_HTMLTag - min_HTMLTag) == 0 else 1.0 + (HTMLTag - min_HTMLTag) / (
                max_HTMLTag - min_HTMLTag)
        Entropy = 1.0 if (max_Entropy - min_Entropy) == 0 else 1.0 + (Entropy - min_Entropy) / (
                max_Entropy - min_Entropy)
        Score = Relevance * Entity * A_Score * Order * Pattern * HTMLTag * Entropy
        max_Score = Score if max_Score < Score else max_Score
        min_Score = Score if min_Score > Score else min_Score
        Normalized_sent_list_tmp.append(
            [sent_Num, raw_sent, sent_without_tag, Relevance, Entity, A_Score, Order, Pattern, HTMLTag, Entropy,
             Score, q_id])
    del sent_list
    # Normalization Score from 0.0 -> 1.0
    Normalized_sent_list = []
    for [sent_Num, raw_sent, sent_without_tag, Relevance, Entity, A_Score, Order, Pattern, HTMLTag, Entropy,
         Score, q_id] in Normalized_sent_list_tmp:
        Score = (Score - min_Score) / (max_Score - min_Score)
        Normalized_sent_list.append(
            [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id])
    del Normalized_sent_list_tmp

    # sort by Score then q_id
    Normalized_sent_list.sort(key=operator.itemgetter(4, 5), reverse=True)
    count = 1
    relevant_paragraphs = []
    for [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id] in Normalized_sent_list:
        if count > top_relevant_paragraph_num:
            break
        relevant_paragraphs.append([sent_Num, raw_sent, sent_without_tag, Order, Score, q_id])
        count += 1
    return relevant_paragraphs


def load_qs_result(rq_fpath):
    import pandas as pd
    rq_res = []
    df = pd.read_csv(rq_fpath)
    for idx, row in df.iterrows():
        rq_res.append([row[0], row[1]])
    return rq_res


if __name__ == '__main__':
    print 'start : ', time.strftime('%Y-%m-%d %H:%M:%S')
    # parameter
    top_relevant_paragraph_num = 10
    rq_res_fpath = os.path.join(res_dir, "rq_res.csv")
    res = []
    for query, top_dq_id in load_qs_result(rq_res_fpath):
        top_ss = get_ss(query, top_relevant_paragraph_num, top_dq_id)
        for i in range(len(top_ss)):
            print("#%s\n%s\n\n" % (i, top_ss[i]))
        res.append([query, top_ss])
    print 'Done. ', time.strftime('%Y-%m-%d %H:%M:%S')
