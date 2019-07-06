#!/usr/bin/python27
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Sat 15 Jul 2017 08:20:12 PM CST
# File Name: get_action_data.py
# Description: 获得用户点击数据
######################################################################
import json
import time
import sys
sys.path.append("/root/base")
import sql_appbk
reload(sys)
sys.setdefaultencoding('utf-8')

def get_action_data():
    sql = "select uid,source_vid from user_action where action='OPEN'"
    result = sql_appbk.mysql_com(sql)
    for item in result:
        print item["uid"] + "\t" + str(item["source_vid"]) + "\t1"


if __name__=="__main__":
    get_action_data()
    
