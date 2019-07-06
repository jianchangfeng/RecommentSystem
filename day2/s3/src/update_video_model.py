#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 11 Jul 2017 04:29:27 PM CST
# File Name: update_user_model.py
# Description:给视频打上类别和关键词标签
######################################################################
import json
import time
import sys
import sql_appbk
import get_classify
import get_tag

"""
功能：获得没有标签的视频信息
输入：无
输出：无
返回：视频信息列表，每一条记录包含视频内部id和标题
"""
def get_video_list():
    sql_com="select id,title from video_info where appbk_sub_category is null"
    result = sql_appbk.mysql_com(sql_com)
    return result

"""
功能：获得一个文本的类别标签和关键词标签
输入：text，一个文本
输出：无
返回：一个list，0，类别标签；1 关键词标签 ， 多个标签之间用英文逗号分隔

"""
def get_tags(text):
    # 获得类别标签
    classes = get_classify.classify(text)

    if -1 == classes:
        classes = ['奇闻趣事']

    classes_str = ",".join(classes)

    # 获得关键词标签
    keywords = get_tag.get_tags(text)
    keywords_str = ",".join(keywords)
    # print keywords_str

    return [classes_str, keywords_str]

"""
功能：更新到数据库
"""
def update_db(vid,appbk_sub_category,appbk_tags):

    sql_com="update video_info set appbk_sub_category='" \
            + appbk_sub_category +"', appbk_tags='" + appbk_tags \
            + "' where id=" + str(vid)
    result = sql_appbk.mysql_com(sql_com)
    return result


"""
功能：主函数，更新用户模型
输入：无
输出：无
"""
def update_video_model():
    #获得所有未处理的视频
    video_list = get_video_list()
    for video in video_list:
        text = video["title"]
        vid = video["id"]
        [classes, keywords] = get_tags(text)
        #更新数据库
        update_db(vid, classes, keywords)
    return 0

if __name__ == '__main__':
    update_video_model()
