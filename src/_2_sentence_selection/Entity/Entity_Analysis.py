# -*- coding: UTF-8 -*-
from _1_question_retrieval.Entity.entity_util import load_entity_dic


def get_entity_score(query_entities, paragraph):
    paragraph = paragraph.split(' ')
    total_num = len(query_entities)
    include_num = 0.0
    if total_num == 0:
        return 1.5
    for query_entity in query_entities:
        if query_entity in paragraph:
            include_num += 1.0
    return 1.0 + (include_num / total_num)


# (sentence text include entities)

def get_entities_from_text(text):
    entity_dic = load_entity_dic()
    word_list = text.split(' ')
    entity_list = []
    for word in word_list:
        if word in entity_dic:
            entity_list.append(word)
    return entity_list