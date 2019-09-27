#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Fri 14 Jul 2017 12:00:16 PM CST
# File Name: user_based_oneline.py
# Description: 使用sql语句,实现简单的基于用户的协同过滤推荐 
######################################################################
import json
import time
import sys
import sql_appbk

"""
功能:实现基于用户的协同过滤推荐
输入:uid
返回:推荐的vid列表
"""


def recommend(uid, limit=10):
    sql = "SELECT source_vid, count(*) as score from user_action right JOIN \
             ( \
            SELECT uid,count(*) as num from user_action where source_vid in \
            (select source_vid FROM user_action where uid='" + uid + "') and uid!='" + uid + "' \
            GROUP BY uid \
            ORDER BY num DESC limit 50 \
            ) as simliar_user \
            on user_action.uid=simliar_user.uid \
            GROUP BY source_vid ORDER BY score DESC limit " + str(limit)

    result = sql_appbk.mysql_com(sql)
    vid_list = []
    for item in result:
        vid_list.append(item["source_vid"])
    return vid_list


if __name__ == "__main__":
    print(recommend("1"))
