#!/usr/bin/env python
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 11 Jul 2017 04:29:27 PM CST
# File Name: get_user_model.py
# Description:从数据库中获得用户模型
######################################################################
import json
import time
import sys
import random
import sql_appbk

"""
功能：得用户的当前类别和关键词标签列表
输入：uid, 用户id
返回：用户的类别和关键词标签列表，每个随机取3个
"""
def get_user_tags(uid):
    sql_com = "SELECT appbk_sub_category,appbk_tags FROM user_tags WHERE uid = '" + str(uid) + "'"
    result = sql_appbk.mysql_com(sql_com)
    if result:
        appbk_sub_category_list = result[0]["appbk_sub_category"].split(",") #类别标签
        appbk_tag_list = result[0]["appbk_tags"].split(",") #关键词标签


        #随机取3个
        category_list = []
        tag_list = []

        if appbk_sub_category_list:#如果有
            category_list = random.sample(appbk_sub_category_list,min(3,len(appbk_sub_category_list)))
        if appbk_tag_list:
            tag_list = random.sample(appbk_tag_list,min(3,len(appbk_tag_list)))
        return {"appbk_sub_category": category_list, "appbk_tags": tag_list}
    else:
        return {"appbk_sub_category": [], "appbk_tags": []}

if __name__=="__main__":
    tags = get_user_tags("maris@appbk.com")
    print (json.dumps(tags))
