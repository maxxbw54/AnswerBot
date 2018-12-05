# -*- coding: utf-8 -*-
import gensim
#from utils.db_util import read_questions_from_repo
from pathConfig import get_base_path

dir_of_entity = get_base_path() + '/_1_question_retrieval/'
path_of_model = dir_of_entity + '_2_word2vecModel/model'


def load_w2v_model():
    word2vector_model = gensim.models.Word2Vec.load(path_of_model)
    return word2vector_model


def load_idf_voccab():
    path = get_base_path() + '/_1_question_retrieval/_3_IDF_vocabulary/idf_vocab.txt'
    file = open(path)
    voc = {}
    for line in file:
        line = line.strip().split(',')
        voc[line[0]] = float(line[1])
    return voc
