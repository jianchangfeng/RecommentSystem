#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Thu 15 Jun 2017 12:13:40 PM CST
# File Name: video_rec.py
# Description:短视频推荐 
######################################################################
import json
import time
import sys
import sql_appbk
import random

# reload(sys)
# sys.setdefaultencoding('utf8')

OSS_URL = "https://shortvedos.oss-cn-beijing.aliyuncs.com/play01/"  # 存储地址

"""
功能：获得一个视频的信息
输入：id，视频内部id
返回：视频信息
"""


def get_video(id):
    final_result = []

    sql = "SELECT id,vid,title,thumbnail,link,duration, \
                bigThumbnail,view_count,appbk_category,source,published \
                FROM video_info WHERE id = " + str(id)
    result = sql_appbk.mysql_com(sql)

    for item in result:
        # 拼接play url
        source = item["source"]
        vid = item["vid"]
        play_url = OSS_URL + source + "_" + vid + ".mp4"
        item["play_url"] = play_url
        final_result.append(item)

    final_result = {"status": 0, "msg": "success", "results": final_result[0]}
    return json.dumps(final_result, cls=sql_appbk.CJsonEncoder)


"""
功能：获得视频推荐列表
输入：c 类别
返回：推荐结果
"""


def get_videos_by_category(c, start=0, limit=10, uid=0, pid=0):
    temp_result = []  # 中间结果

    # 获得热门推荐
    vid_list = get_hot_videos(c)
    id_list_str = ",".join(vid_list)

    sql = "SELECT id,vid,title,thumbnail,link,duration, \
            bigThumbnail,view_count,appbk_category,source,published \
            FROM video_info WHERE id in (" + id_list_str + ")"
    result = sql_appbk.mysql_com(sql)

    for item in result:
        # 拼接play url
        source = item["source"]
        vid = item["vid"]
        play_url = OSS_URL + source + "_" + vid + ".mp4"
        item["play_url"] = play_url
        temp_result.append(item)

    # 随机打乱
    random.shuffle(temp_result)

    final_result = {"status": 0, "msg": "success", "results": temp_result[int(start):int(start) + int(limit)]}
    return json.dumps(final_result, cls=sql_appbk.CJsonEncoder)


"""
功能：获得热门推荐结果
输入：c 类别
返回：推荐结果
"""


def get_hot_videos(c, limit=400):
    # 取7天内的结果, limit取足够大
    start_day = time.strftime('%Y-%m-%d', time.localtime(time.time() - 7 * 24 * 60 * 60))
    sql = "SELECT id,vid,title,thumbnail,link,duration, \
            bigThumbnail,view_count,appbk_category,source,published \
            FROM video_info WHERE down_action_time>'" + start_day + "' \
            and appbk_category='" + c + "' \
            ORDER BY view_count DESC \
            limit " + str(limit)
    result = sql_appbk.mysql_com(sql)
    print(result)
    vid_list = []
    for item in result:
        vid_list.append(str(item["id"]))
    return vid_list


if __name__ == "__main__":
    # sql_com ="select * from video_info_test limit 10"
    # result = sql_appbk.mysql_com(sql_com)
    # print json.dumps(result,cls=sql_appbk.CJsonEncoder)
    c = '游戏'
    print(get_videos_by_category(c))
