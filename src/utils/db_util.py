# -*- coding: UTF-8 -*-

import MySQLdb as mdb
from data_structure.SO_QuestionUnit import SO_QuestionUnit
from data_structure.SO_AnswerUnit import SO_AnswerUnit
from data_util import preprocessing_for_SO_QuestionUnit, preprocessing_for_SO_AnswerUnit
from utils.remove_StopWords import remove_stopwords
from utils.Stemming import stemming_for_word_list


# java
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
            # id,type,title,tag
            SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[11], '', '', row[12])
            SO_QuestionUnit_tmp = preprocessing_for_SO_QuestionUnit(SO_QuestionUnit_tmp)
            SO_datalist.append(SO_QuestionUnit_tmp)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_datalist


# repo
def read_questions_from_repo(num):
    sql = 'SELECT * FROM GeneralAnswer.repo WHERE PostTypeId=1 limit 0,' + str(num)
    SO_datalist = []
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    try:
        cur.execute(sql)
        results = cur.fetchall()
        count = 0
        for row in results:
            count += 1
            # id,type,title,title_NO_SW,title_NO_SW_Stem,tag
            SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[2], row[3], row[4], row[5])
            SO_datalist.append(SO_QuestionUnit_tmp)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_datalist


def read_all_questions_from_post():
    sql = 'SELECT * FROM posts where Tags like \'%<java>%\' and AnswerCount > 0'
    SO_datalist = []
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    try:
        cur.execute(sql)
        results = cur.fetchall()
        count = 0
        for row in results:
            count += 1
            # id,type,title,title_NO_SW,title_NO_SW_Stem,tag
            SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[2], row[3], row[4], row[5])
            SO_datalist.append(SO_QuestionUnit_tmp)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_datalist


# repo
def read_all_questions_from_repo():
    sql = 'SELECT * FROM repo'
    SO_datalist = []
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    try:
        cur.execute(sql)
        results = cur.fetchall()
        count = 0
        for row in results:
            count += 1
            # id,type,title,title_NO_SW,title_NO_SW_Stem,tag
            SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[2], row[3], row[4], row[5])
            SO_datalist.append(SO_QuestionUnit_tmp)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_datalist


def read_specific_question_from_repo(id):
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    sql = "SELECT * FROM repo WHERE Id=" + str(id)
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            # id,type,title,title_NO_SW,title_NO_SW_Stem,tag
            SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[2], row[3], row[4], row[5])
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_QuestionUnit_tmp

def read_specific_question_from_post(id):
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    sql = "SELECT * FROM posts WHERE Id=" + str(id)
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            # id,type,title,title_NO_SW,title_NO_SW_Stem,tag
            SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[2], row[3], row[4], row[5])
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_QuestionUnit_tmp


def read_specific_question_from_post(id):
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    sql = "SELECT * FROM posts WHERE Id=" + str(id)
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            # id,type,title,tag
            SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[11], '', '', row[12])
            SO_QuestionUnit_tmp = preprocessing_for_SO_QuestionUnit(SO_QuestionUnit_tmp)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return SO_QuestionUnit_tmp


def read_duplicate_pair_from_postlink_table(num):
    Duplicate_pair = []
    postlink_sql = "SELECT * FROM post_links ORDER BY PostId"
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    try:
        cur.execute(postlink_sql)
        results = cur.fetchall()
        count = 1
        for row in results:
            id1 = row[2]
            if ifjava_post(id1) == False:
                continue
            id2 = row[3]
            if ifjava_post(id2) == False:
                continue
            Duplicate_pair.append([id1, id2])
            print 'processing ' + str(count)
            if count >= num:
                break
            count += 1
            # total size : 236616 (java)
            # size = len(results)
            # 160000 as train
            # 40000 as test
    except Exception as e:
        print e
    cur.close()
    con.close()
    return Duplicate_pair


def ifjava_post(id):
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    sql = "SELECT * FROM posts WHERE Id=" + str(id) + " and Tags like '%<java>%'"
    ifjava = False
    try:
        cur.execute(sql)
        results = cur.fetchall()
        if len(results) != 0:
            ifjava = True
    except Exception as e:
        print e
    cur.close()
    con.close()
    return ifjava


def read_correspond_answer_from_java_table(q_id):
    corr_answer = []
    sql = "SELECT * FROM java WHERE PostTypeId = 2 AND ParentId = " + str(q_id)
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            # id, type, score, desc
            SO_AnswerUnit_tmp = SO_AnswerUnit(row[0], row[1], row[4], row[6])
            SO_AnswerUnit_tmp = preprocessing_for_SO_AnswerUnit(SO_AnswerUnit_tmp)
            corr_answer.append(SO_AnswerUnit_tmp)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return corr_answer


def read_java_pair_from_postlink():
    sql = "SELECT * FROM post_links"
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    post_pair = []
    post_list = []
    count = 0
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            if count % 10000 == 0:
                print 'count : ' + str(count)
            count += 1
            postId = row[2]
            related_postId = row[3]
            linktypeId = row[4]
            if ifjava_post(postId) and ifjava_post(related_postId):
                post_pair.append([postId, related_postId, linktypeId])
                if postId not in post_list:
                    post_list.append(postId)
                if related_postId not in post_list:
                    post_list.append(related_postId)
    except Exception as e:
        print e
    cur.close()
    con.close()
    return post_pair, post_list


def read_id_list_from_java(id_list):
    SO_QuestionUnit_list = []
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    count = 1
    for id in id_list:
        if count % 10000 == 0:
            print 'reading ' + str(count) + ' question from Table java'
        count += 1
        sql = "SELECT * FROM java WHERE Id=" + str(id) + ";"
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                # id,type,title,tag
                SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[11], '', '', row[12])
                SO_QuestionUnit_tmp = preprocessing_for_SO_QuestionUnit(SO_QuestionUnit_tmp)
                SO_QuestionUnit_list.append(SO_QuestionUnit_tmp)
        except Exception as e:
            print e
    cur.close()
    con.close()
    return SO_QuestionUnit_list


# repo
def insert_SO_QuestionUnit_List_to_repo(SO_QuestionUnit_list, stopwords):
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    count = 1
    for SO_QuestionUnit in SO_QuestionUnit_list:
        title_without_stopwords = remove_stopwords(SO_QuestionUnit.title.split(' '), stopwords)
        str_title_without_stopwords = " ".join(str(x) for x in title_without_stopwords)
        title_without_stopwords_stemming = stemming_for_word_list(title_without_stopwords)
        str_title_without_stopwords_stemming = " ".join(str(x) for x in title_without_stopwords_stemming)
        if count % 10000 == 0:
            print 'inserting ' + str(count) + ' question to Table repo'
        count += 1
        # id,type,title,desc,tag
        sql = 'INSERT INTO repo VALUES(\'' + str(SO_QuestionUnit.id) + '\',\'' + str(
            SO_QuestionUnit.type) + '\',\'' + str(SO_QuestionUnit.title) + '\',\'' + str(
            str_title_without_stopwords) + '\',\'' + str(str_title_without_stopwords_stemming) + '\',\'' + str(
            SO_QuestionUnit.tag) + '\')'
        try:
            cur.execute(sql)
            con.commit()
        except Exception as e:
            print e
    cur.close()
    con.close()
    print 'insert Done.'


# repo
def read_id_list_from_repo(id_list):
    SO_QuestionUnit_list = []
    con = mdb.connect('localhost', 'root', '123456', 'GeneralAnswer')
    cur = con.cursor()
    count = 1
    for id in id_list:
        if count % 10000 == 0:
            print 'reading ' + str(count) + ' question from Table repo'
        count += 1
        sql = "SELECT * FROM repo WHERE Id=" + str(id)
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                # id,type,title,title_NO_SW,title_NO_SW_Stem,tag
                SO_QuestionUnit_tmp = SO_QuestionUnit(row[0], row[1], row[2], row[3], row[4], row[5])
                SO_QuestionUnit_list.append(SO_QuestionUnit_tmp)
        except Exception as e:
            print e
    cur.close()
    con.close()
    return SO_QuestionUnit_list
