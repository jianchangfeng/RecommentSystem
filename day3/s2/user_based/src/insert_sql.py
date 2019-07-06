#!/usr/bin/env python
#coding=utf-8
import os
import sys
import time
import json
import urllib2
import urllib
import ConfigParser
import logging
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
#插入数据库
#输入文件名，表名，文件为json格式的文件，一行一个记录

def publish_data(data, table_name):
    db_name = "short_video"
    db_host = "rm-bp1w81w3y5da24ape.mysql.rds.aliyuncs.com"
    db_user = "rootali"
    db_pw = "Rootali1"
    try:
        db = MySQLdb.connect(host = db_host, user=db_user, passwd = db_pw, db = db_name, charset='utf8')
    except Exception as e:
        print "mysql login error ", e
        return -1

    cursor = db.cursor()
    
    sqlcom = ""
    key_list = []
    value_list = []
    for item in data:
        key_list.append(item)
        value_list.append("'" +  db.escape_string( str(data[item])) + "'")
    key = ",".join(key_list)
    value = ",".join(value_list)

    #sqlcom = "replace into  " +  table_name + " (" + key + ") values (" + value + ")" 
    sqlcom = "INSERT ignore into  " + table_name + " (" + key + ") values (" + value + ") " 
    #print sqlcom
    cursor.execute(sqlcom)
    insert_id = int(db.insert_id()) #插入的自增id
    db.commit()
    db.close()
    return insert_id

if __name__=="__main__":
    if len(sys.argv)!=3:
        print "please input filename and table name"
        sys.exit() 

    data_file = open(sys.argv[1], 'r')
    table_name = sys.argv[2]

    for line in data_file:
        line = line.strip()
        try:
            data = json.loads(line)
        except:
            continue
        try:
            publish_data(data, table_name)
        except Exception as e:
            print "insert error ", e
            continue

