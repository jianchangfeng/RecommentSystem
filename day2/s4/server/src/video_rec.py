#!/usr/bin/env python
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Thu 15 Jun 2017 12:13:40 PM CST
# File Name: video_rec.py
# Description:短视频推荐 
######################################################################
import json
import time
import sys
import get_user_model #用户模型
import ali_search #阿里云搜索
import sql_appbk
import random

OSS_URL = "http://appbkplay.oss-cn-hangzhou.aliyuncs.com/play1/" #存储地址

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
def get_videos_by_category(c,start=0,limit=10,uid="0", pid="0"):
    temp_result = [] #中间结果

    #获得热门推荐
    vid_list = get_hot_videos(c, 30)

    #获得基于内容的推荐
    content_based_videos = get_content_based_videos(uid, 30)
    vid_list.extend(content_based_videos)

    #查询视频元数据
    if len(vid_list)>0:
        id_list_str = ",".join(vid_list)
        sql = "SELECT id,vid,title,thumbnail,link,duration, \
                bigThumbnail,view_count,appbk_category,source,published \
                FROM video_info WHERE id in ("+ id_list_str +")"
    else:
        sql = "SELECT id,vid,title,thumbnail,link,duration, \
                bigThumbnail,view_count,appbk_category,source,published \
                FROM video_info limit 100" #如果没有推荐，随机选择一些

    result = sql_appbk.mysql_com(sql)

    for item in result:
        #拼接play url
        source = item["source"]
        vid = item["vid"]
        play_url = OSS_URL + source+ "_" + vid + ".mp4"
        item["play_url"] = play_url
        temp_result.append(item)

    #随机打乱,规则处理
    random.shuffle(temp_result)

    final_result = {"status":0,"msg":"success","results":temp_result[int(start):int(start)+int(limit)]}
    return json.dumps(final_result,cls=sql_appbk.CJsonEncoder)

"""
功能：获得热门推荐结果
输入：c 类别
返回：推荐结果,vid列表
"""
def get_hot_videos(c, limit=400):
    #取三天内的结果, limit取足够大
    start_day = time.strftime('%Y-%m-%d', time.localtime(time.time()-3*24*60*60))
    sql = "SELECT id,vid,title,thumbnail,link,duration, \
            bigThumbnail,view_count,appbk_category,source,published \
            FROM video_info WHERE down_action_time>'"+ start_day+ "' \
            and appbk_category='"+ c +"' \
            ORDER BY view_count DESC \
            limit " + str(limit)
    result = sql_appbk.mysql_com(sql)
    vid_list = []
    for item in result:
        vid_list.append(str(item["id"]))
    return vid_list

"""
功能：获得基于内容的推荐结果
输入：uid， 用户id
输入：limit，取多少个
返回：推荐结果，vid列表
"""
def get_content_based_videos(uid, limit=10):
    vid_list = []
    #step1，获得用户模型
    user_model = get_user_model.get_user_tags(uid)
    appbk_sub_category = user_model["appbk_sub_category"]
    appbk_tags = user_model["appbk_tags"]

    #step 2,根据类别，取数据
    appbk_sub_category_sql = ",".join(["'"+item+"'" for item in appbk_sub_category])
    if appbk_sub_category: #不为空
        sql = "SELECT id,vid,title,thumbnail,link,duration, \
                bigThumbnail,view_count,appbk_category,source,published \
                FROM video_info WHERE appbk_sub_category in ("+ appbk_sub_category_sql +") limit 20"
        result = sql_appbk.mysql_com(sql)
        for item in result:
            vid_list.append(str(item["id"]))

    #step 3,根据关键词标签搜索结果
    if len(appbk_tags)>0:
        search_result = ali_search.search(appbk_tags,20)
        for item in search_result:
            vid_list.append(str(item["id"]))

    #随机打乱
    random.shuffle(vid_list)

    return vid_list[0:limit]

"""
功能：添加用户行为
输入：uid， 用户id
输入：id，视频id
输入：action，用户行为
返回：成功信息
"""
def add_user_action(uid, id, action="OPEN"):
    sql = "INSERT INTO user_action (uid,source_vid,update_time,action) \
           VALUES \
           ('"+str(uid)+"',"+id+",NOW(),'OPEN')"
    result = sql_appbk.mysql_com(sql)
    return json.dumps({"status":0,"msg":"success"})

if __name__ == "__main__":
    c = '搞笑'
    uid = "maris@appbk.com"
    print(get_videos_by_category(c,0,10,uid,0))

