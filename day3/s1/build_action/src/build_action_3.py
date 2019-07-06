#!/usr/bin/env python
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Fri 14 Jul 2017 11:40:16 AM CST
# File Name: build_action.py
# Description: 构造用户行为数据
######################################################################
import json
import time
import sys
import sql_appbk

"""
功能:获得短视频id,已经下载的
输入:
输出:
返回: 视频id list
"""
def get_video_id():
    video_id_list = []
    sql = "select id from video_info where is_download=1 limit 1700"
    result = sql_appbk.mysql_com(sql)
    for item in result:
        video_id_list.append(item["id"])
    return video_id_list

"""
功能:读取mv的用户行为数据,构造新的行为数据
输入: mv的文件名
输出:
返回: 
"""
def build_action(filename):
    #获得短视频id
    video_id_list = get_video_id()

    data_file = open(filename, "r")
    for line in data_file:
        line = line.strip()
        item = line.split()
        ori_uid = item[0]
        ori_vid = item[1]
        uid = ori_uid #用户id和原始的保持一致
        vid = video_id_list[int(ori_vid)-1] #vid按照顺序依次对应
        user_action = {}
        user_action["uid"] = uid
        user_action["source_vid"] = vid
        user_action["action"] = "OPEN"
        #print (json.dumps(user_action)) #生成json数据,使用insert_sql.py插入,速度很慢
        print (str(uid) + "\t" + str(vid) + "\tOPEN") #直接load

if __name__=="__main__":
    if 2!=len(sys.argv):
        print ("please input filename")
        sys.exit()

    filename = sys.argv[1]
    build_action(filename)
