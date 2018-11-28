# coding=utf-8
from util.db_util import read_table

from util.file_util import write_file

path_of_Corpus = 'textual_corpus.txt'

if __name__ == '__main__':
    str = ''
    sql = 'SELECT * FROM GeneralAnswer.java WHERE PostTypeId=1 limit 0,1000000'
    SO_datalist = read_table(sql)
    for SO_data_tmp in SO_datalist:
        str += SO_data_tmp.title + " "
        str += SO_data_tmp.desc + "\n"
    write_file(path_of_Corpus, str.strip())
    print 'Done'
