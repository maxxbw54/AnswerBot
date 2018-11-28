# -*- coding: utf-8 -*-
import MySQLdb as mdb
from utils.file_util import write_file


def extract_tag_info_from_java_table(num):
    sql = 'SELECT * FROM GeneralAnswer.java WHERE PostTypeId=1 limit 0,' + str(num)
    con = mdb.connect('localhost', 'root', 'root', 'GeneralAnswer')
    cur = con.cursor()
    dic = []
    Corpus = ''
    try:
        cur.execute(sql)
        results = cur.fetchall()
        count = 0
        for row in results:
            if count % 1000 == 0:
                print 'processing ' + str(count) + ' instance'
            count += 1
            # tag : '<java><xml><csv><data-conversion>'
            tag_list_tmp = row[12].replace('<', ' ').replace('>', ' ').replace('  ', ' ').strip()
            Corpus += (tag_list_tmp + '\n')
            tag_list_tmp = tag_list_tmp.split(' ')
            for tag_tmp in tag_list_tmp:
                if tag_tmp not in dic:
                    dic.append(tag_tmp)
    except Exception as e:
        print e
    con.close()
    return dic, Corpus


if __name__ == '__main__':
    num = 1000000
    path_of_dic = 'entity_dic.txt'
    path_of_corpus = 'entity_corpus.txt'
    dic, Corpus = extract_tag_info_from_java_table(num)
    dic_str = ''
    for tag_tmp in dic:
        dic_str += (tag_tmp + '\n')
    write_file(path_of_dic, dic_str)
    write_file(path_of_corpus, Corpus)
    print 'Done.'
