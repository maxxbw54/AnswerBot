# -*- coding: utf-8 -*-

from data_structure.SO_que import SO_Que
from utils.file_util import write_file
import pymysql as mdb
from utils.data_util import preprocessing_for_SO_QuestionUnit

path_of_Corpus = 'textual_corpus.txt'


def read_questions_from_java(num):
    sql = 'SELECT * FROM GeneralAnswer.java WHERE PostTypeId=1 limit 0,' + str(num)
    SO_datalist = []
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    try:
        cur.execute(sql)
        results = cur.fetchall()
        count = 0
        for row in results:
            count += 1
            # id,title,desc,tag
            SO_QuestionUnit_tmp = SO_Que(row[0], row[15], row[8], row[16])
            SO_QuestionUnit_tmp = preprocessing_for_SO_QuestionUnit(SO_QuestionUnit_tmp)
            SO_datalist.append(SO_QuestionUnit_tmp)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_datalist


if __name__ == '__main__':
    str = ''
    num = 1000000
    SO_datalist = read_questions_from_java(num=1000000)
    for SO_data_tmp in SO_datalist:
        str += SO_data_tmp.title + " "
        str += SO_data_tmp.desc + "\n"
    write_file(path_of_Corpus, str.strip())
    print 'Done'
