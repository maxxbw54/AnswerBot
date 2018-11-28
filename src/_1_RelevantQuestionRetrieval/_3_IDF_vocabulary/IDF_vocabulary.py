# -*- coding: utf-8 -*-
from util.db_util import read_all_questions_from_repo
import math
from util.file_util import write_file
from pathutil import get_base_path


def build_IDF_vocabulary():
    SO_QuestionUnit_List = read_all_questions_from_repo()
    total_num = len(SO_QuestionUnit_List)
    voc = {}
    write_str = ''
    count = 0
    for SO_QuestionUnit in SO_QuestionUnit_List:
        count += 1
        title_word_list = SO_QuestionUnit.title.strip().split(' ')
        cur_word_list = []
        for word in title_word_list:
            if word not in cur_word_list:
                cur_word_list.append(word)
                if word not in voc.keys():
                    voc[word] = 1.0
                else:
                    voc[word] = voc[word] + 1.0
    for key in voc.keys():
        idf = math.log(total_num / (voc[key] + 1.0))
        write_str += (str(key) + ' ' + str(idf) + '\n')
    path = 'idf_voc.txt'
    write_file(path, write_str)


if __name__ == '__main__':
    build_IDF_vocabulary()
    print 'Done.'
