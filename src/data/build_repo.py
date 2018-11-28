# -*- coding: UTF-8 -*-

from util.file_util import read_sentence_by_line
from util.db_util import read_id_list_from_java, insert_SO_QuestionUnit_List_to_repo

''' SQL :  CREAT TABLE
CREATE TABLE repo (
    Id INT NOT NULL PRIMARY KEY,
    PostTypeId INT,
	Title text NULL,
	Title_No_SW text NULL,
	Title_No_SW_Stem text NULL,
	Tags VARCHAR(256)
);

create index repo_idx_1 on repo(Id);

'''
from util.remove_StopWords import read_EN_stopwords

if __name__ == '__main__':
    path_of_id_list = 'post_id_list.txt'
    id_list = read_sentence_by_line(path_of_id_list)
    SO_QuestionUnit_List = read_id_list_from_java(id_list)
    #print SO_QuestionUnit_List
    stopwords = read_EN_stopwords()
    insert_SO_QuestionUnit_List_to_repo(SO_QuestionUnit_List, stopwords)
