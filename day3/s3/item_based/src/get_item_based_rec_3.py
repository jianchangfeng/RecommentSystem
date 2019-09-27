#!/usr/bin/env python3
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Sun 16 Jul 2017 12:07:21 PM CST
# File Name: get_item_based_rec.py
# Description: 获得基于物品的推荐结果
######################################################################
import json
import time
import sys

sys.path.append("/root/base")
import sql_appbk

"""
功能:获得基于用户的推荐
输入:uid, 用户id
返回:推荐的视频id列表
"""


def get_item_based_rec(uid):
    vid_list = []
    sql = "SELECT vid,sum(sim) as score from ( \
                ( \
                    SELECT vid2 as vid,sim from item_based_rec WHERE vid1 in \
                        (SELECT * FROM \
                            ( \
                                select source_vid from user_action  where uid='" + uid + "' ORDER BY rand() limit 10 \
                            ) as vid_list) \
                ) \
                UNION \
                ( \
                    SELECT vid1 as vid,sim from item_based_rec WHERE vid2 in \
                        (SELECT * FROM  \
                            ( \
                                select source_vid from user_action  where uid='" + uid + "' ORDER BY rand() limit 10 \
                            ) as vid_list \
                        ) \
                ) \
        ) as vid_score group by vid ORDER BY score desc LIMIT 100"
    result = sql_appbk.mysql_com(sql)
    for item in result:
        vid_list.append(item["vid"])
    return vid_list


if __name__ == "__main__":
    print(get_item_based_rec("1"))
