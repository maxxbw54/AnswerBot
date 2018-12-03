# -*- coding: utf-8 -*-
from utils.db_util import read_all_questions_from_repo
import math
from utils.file_util import write_file
from nltk import word_tokenize


def build_IDF_vocabulary():
    qlist = read_all_questions_from_repo()
    total_num = len(qlist)
    voc = {}
    write_str = ''
    count = 0
    for q in qlist:
        title_wlist = word_tokenize(q.title.strip())
        cur_word_list = []
        for w in title_wlist:
            if w not in cur_word_list:
                cur_word_list.append(w)
                if w not in voc.keys():
                    voc[w] = 1.0
                else:
                    voc[w] = voc[w] + 1.0
        count += 1
        if count % 3000 == 0:
            print 'processing %s unit...' % count
    for key in voc.keys():
        idf = math.log(total_num / (voc[key] + 1.0))
        write_str += (str(key) + ',' + str(idf) + '\n')
    path = 'idf_vocab.txt'
    write_file(path, write_str)


if __name__ == '__main__':
    build_IDF_vocabulary()
    print 'Done.'
