#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Sun 16 Jul 2017 12:07:21 PM CST
# File Name: get_user_based_rec.py
# Description: 获得基于用户的推荐结果
######################################################################
import json
import time
import sys
import sql_appbk

"""
功能:获得基于用户的推荐
输入:uid, 用户id
返回:推荐的视频id列表
"""


def get_user_based_rec(uid):
    vid_list = []
    sql = "select vid from user_based_rec where uid='" + uid + "'"
    result = sql_appbk.mysql_com(sql)
    if result:
        vids = result[0]["vid"]
        vid_list = vids.split(",")

    return vid_list


if __name__ == "__main__":
    print(get_user_based_rec("1"))
