#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 11 Jul 2017 04:29:27 PM CST
# File Name: update_user_model.py
# Description:从数据库里抽取用户看过的视频，基于这些视频给用户提取类别和关键词标签
######################################################################
import json
import time
import sys
import sql_appbk
import get_classify
import get_tag


"""
功能：获得用户未处理的访问记录，将未访问记录的is_processed 变为1
输入：无
输出：用户的未处理的行为列表
"""
def get_user_actions():
    #获得未处理的用户行为记录
    sql_com = "select * from user_action where is_processed=0"
    result = sql_appbk.mysql_com(sql_com)

    #更新已处理的记录
    sql_com = "UPDATE user_action set is_processed = 1 WHERE is_processed=0"
    sql_appbk.mysql_com(sql_com)
    return result


"""
功能：获得一条视频信息
输入：vid, 视频id
返回：视频信息列表，每一条记录包含视频内部id和标题
"""
def get_video_info(vid):
    sql_com = "select id,title from video_info where id =" + str(vid)
    result = sql_appbk.mysql_com(sql_com)
    return result[0]


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
功能：得用户的当前类别和关键词标签列表
输入：用户id
返回：用户的类别和关键词标签列表
"""

def get_user_tags(uid):
    sql_com = "SELECT appbk_sub_category,appbk_tags FROM user_tags WHERE uid = '" + str(uid) + "'"
    result = sql_appbk.mysql_com(sql_com)
    if result:
        return result[0]
    else:
        return {"appbk_sub_category": "", "appbk_tags": ""}


"""
功能：合并用户的标签，新的附加到旧的，保留最新的100个
输入：old_tags，之前标签列表，逗号分隔
输入：new_tags，新的标签列表，逗号分隔
返回：合并后的标签列表，逗号分隔
"""
def combine(old_tags, new_tags):
    if not old_tags:#如果不为空
        tag_list = []
    else:
        tag_list = old_tags.split(",")

    if ""!=new_tags:
        tag_list.extend(new_tags.split(","))

    if 0 == len(tag_list):
        return ""

    max_len = 100
    if len(tag_list) <= max_len:
        return ",".join(tag_list)
    else:
        return ",".join(tag_list[len(tag_list) - max_len:])


"""
功能：根据用户模型数据
输入：uid, 用户id
输入：appbk_new_sub_category，新的类别
输入：appbk_new_tags， 新的关键词标签
返回：更新结果

"""
def update_db(uid, appbk_new_sub_category, appbk_new_tags):
    # 获得当前时间
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    sql_com = "replace into user_tags(uid ,appbk_sub_category ,appbk_tags,update_time)\
            VALUES('" + str(
        uid) + "' , '" + appbk_new_sub_category + "' , '" + appbk_new_tags + "' , '" + update_time + "')"
    result = sql_appbk.mysql_com(sql_com)
    return result


"""
功能：主函数，更新用户模型
输入：无
输出：无
"""
def update_user_model():
    # step1 获得所有未处理的访问记录，将未访问记录的is_processed 变为1
    action_list = get_user_actions()
    print(action_list)
    # 处理每条记录
    for action in action_list:
        vid = action["source_vid"] #视频id
        uid = action["uid"] #用户id
        #获得视频信息
        video_info = get_video_info(vid)
        text = video_info["title"]

        # 根据访问记录抽取类别和关键词标签
        [classes, keywords] = get_tags(text)
        print(classes,keywords)

        # step2 合并类别标签和关键词标签
        # 有新的关键词直接添加到原有关键词后面，关键词标签最多保留100个.类别标签同理
        user_tag = get_user_tags(uid)
        appbk_sub_category = user_tag["appbk_sub_category"]
        appbk_tags = user_tag["appbk_tags"]

        #旧的和新的合并
        appbk_new_sub_category = combine(appbk_sub_category, classes)
        appbk_new_tags = combine(appbk_tags, keywords)

        #print appbk_new_sub_category,appbk_new_tags

        # step4 合并到数据库
        ret = update_db(uid, appbk_new_sub_category, appbk_new_tags)



if __name__ == '__main__':
    update_user_model()

