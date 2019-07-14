#!/usr/bin/python
# coding=utf-8
# 功能，appbk数据库访问
# 输入数据库表和sql命令，返回结果
import os
import sys
import time
import json
import datetime
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb

# g_db_host = "rm-bp1w81w3y5da24ape.mysql.rds.aliyuncs.com" #线上机器
# g_db_user = "rootali"
# g_db_pw = "Rootali1"
# g_db_name = "short_video" #数据库名

g_db_host = "10.192.208.176"  # 线上机器
g_db_user = "root"
g_db_pw = "Jcfcxl_1314"
g_db_name = "short_video"  # 数据库名

"""
功能：解决datatime字段输不出json格式错误
"""


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


"""
功能：连接数据
"""


def connect_db():
    db = ''
    try:
        db = MySQLdb.connect(host=g_db_host, user=g_db_user, passwd=g_db_pw, db=g_db_name, charset='utf8',
                             connect_timeout=10)
    except Exception as e:
        print(e)
        return '-1'

    return db


"""
功能：执行mysql命令，返回结果
输入：sql_com, sql命令
返回：mysql查询结果数组
"""


def mysql_com(sql_com):
    # 连接数据库
    for i in range(3):
        db = connect_db()

        if db:
            break
        else:
            i = i + 1

    result = []
    if db != '-1':
        # 执行mysql命令
        # cursor = db.cursor()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_com)
        result = cursor.fetchall()
        db.commit()
        db.close()
    return result


"""
功能：执行mysql插入命令
输入：data， 需要插入的数据，list，每行数据为dict，key为数据库字段名，value为数据值
输入：table_name, 数据库名
返回：mysql查询结果数组
"""


def insert_data(data, table_name):
    # 连接数据库
    for i in range(3):
        db = connect_db()

        if db:
            break
        else:
            i = i + 1

    if db == '-1':
        return -1

    cursor = db.cursor()

    sqlcom = ""
    key_list = []
    value_list = []
    for item in data:
        key_list.append(item)
        value_list.append("'" + db.escape_string(str(data[item])) + "'")
    key = ",".join(key_list)
    value = ",".join(value_list)

    sqlcom = "replace into  " + table_name + " (" + key + ") values (" + value + ")"
    try:
        cursor.execute(sqlcom)
        insert_id = int(db.insert_id())  # 插入的自增id
        db.commit()
        db.close()
        return insert_id
    except Exception as e:
        return e


if __name__ == "__main__":
    sql_com = 'select * from video_info limit 10'
    result = mysql_com(sql_com)
    for row in result:
        print(row["title"])
        # print row[0],'\t',row[1],'\t',row[2],'\t',row[3],'\t',row[4]
