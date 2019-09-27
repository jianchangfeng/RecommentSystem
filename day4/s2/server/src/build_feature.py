#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 11 Jul 2017 04:29:27 PM CST
# File Name: build_feature.py
# Description:构建ctr所需的特征模型
######################################################################
import json
import time
import sys
import sql_appbk
import get_classify
import get_tag

feature_name_id_dict = {}
"""
功能：获得用户未处理的访问记录，将未访问记录的is_processed 变为1
输入：无
输出：用户的未处理的行为列表
"""


def get_user_actions():
    # 获得未处理的用户行为记录
    sql_com = "select * from user_action_ctr"
    result = sql_appbk.mysql_com(sql_com)
    return result


"""
功能：构造特征词典
输入：word_file，关键词字典文件
输入：category_file, 类别词典
输入：source_file, 视频来源
返回：0
"""


def load_feature_id(word_file="idf.dict", category_file="category.dat", source_file="source.dat"):
    feature_id = 1

    # 用户特征,关键词特征id
    input_file = open(word_file, 'r')
    for line in input_file:
        line = line.strip()
        item_list = line.split()
        word = "uw_" + item_list[0]
        feature_name_id_dict[word] = feature_id
        feature_id += 1
    input_file.close()

    # 用户特征,类别特征id
    input_file = open(category_file, 'r')
    for line in input_file:
        line = line.strip()
        item_list = line.split()
        category = "uc_" + item_list[1]
        feature_name_id_dict[category] = feature_id
        feature_id += 1
    input_file.close()

    # 用户特征,用浏览数
    feature_name_id_dict["uv"] = feature_id
    feature_id += 1

    # 视频特征，关键词特征id
    input_file = open(word_file, 'r')
    for line in input_file:
        line = line.strip()
        item_list = line.split()
        word = "vw_" + item_list[0]
        feature_name_id_dict[word] = feature_id
        feature_id += 1
    input_file.close()

    # 视频特征，类别特征id
    input_file = open(category_file, 'r')
    for line in input_file:
        line = line.strip()
        item_list = line.split()
        category = "vc_" + item_list[1]
        feature_name_id_dict[category] = feature_id
        feature_id += 1
    input_file.close()

    # 视频特征，来源
    input_file = open(source_file, 'r')
    for line in input_file:
        source = "s_" + line.strip()
        feature_name_id_dict[source] = feature_id
        feature_id += 1
    input_file.close()

    # 视频特征，视频时长
    feature_name_id_dict["duration_second"] = feature_id
    feature_id += 1

    # 视频特征，标题长度
    feature_name_id_dict["title_length"] = feature_id
    feature_id += 1

    # 场景特征, 用户关键词和视频关键词重复数
    feature_name_id_dict["keyword_match"] = feature_id
    feature_id += 1

    # 场景特征,用户类别和视频类别重复数
    feature_name_id_dict["category_match"] = feature_id
    feature_id += 1

    # 场景特征，用户浏览视频的时间点
    for i in range(0, 24):
        hour_feature = "hour_" + str(i)
        feature_name_id_dict[hour_feature] = feature_id
        feature_id += 1

    return 0


"""
功能：得用户的当前类别和关键词标签列表
输入：用户id
返回：用户的类别和关键词标签列表
"""


def get_user_tags(uid):
    sql_com = "SELECT appbk_sub_category,appbk_tags FROM user_tags_ctr WHERE uid = '" + str(uid) + "'"
    result = sql_appbk.mysql_com(sql_com)
    if result:
        return result[0]
    else:
        return {"appbk_sub_category": "", "appbk_tags": ""}


"""
功能：获得用信息
输入：uid，用户id
返回：用户信息，dict，key为特征名
"""


def get_user_info(uid):
    # 获得用户标签
    user_info = get_user_tags(uid)

    # 获得用浏览视频数
    try:
        sql_com = "select count(*) as num from user_action_ctr where uid =" + str(uid)
        result = sql_appbk.mysql_com(sql_com)
        user_info["uv"] = result[0]["num"]
    except:
        user_info["uv"] = 0
    return user_info


"""
功能：获得一条视频信息
输入：vid, 视频id
返回：视频信息列表，每一条记录包含视频内部id和标题
"""


def get_video_info(vid):
    video_info = {}
    sql_com = "select * from video_info_ctr where id =" + str(vid)
    result = sql_appbk.mysql_com(sql_com)
    if result:
        video_info["appbk_sub_category"] = result[0]["appbk_sub_category"]
        video_info["appbk_tags"] = result[0]["appbk_tags"]
        video_info["source"] = result[0]["source"]
        video_info["duration"] = result[0]["duration"]
        video_info["title_length"] = len(result[0]["title"])
    return video_info


"""
功能：获得场景信息
输入：
返回：
"""


def get_scene_info(action, user_info, video_info):
    scene_info = {}
    # 获得用户关键词和视频关键词重复数
    keyword_match = 0
    user_keyword_list = user_info["appbk_tags"].split(",")
    video_keyword_list = video_info["appbk_tags"].split(",")

    scene_info["keyword_match"] = len(list(set(user_keyword_list).intersection(set(video_keyword_list))))  # 交集

    # 获得用户类别和视频类别重复数
    user_category_list = user_info["appbk_sub_category"].split(",")
    video_category_list = video_info["appbk_sub_category"].split(",")

    scene_info["category_match"] = len(list(set(user_category_list).intersection(set(video_category_list))))  # 交集

    # 获得用户浏览视频的时间点
    scene_info["hour"] = int(action["update_time"].hour)
    return scene_info


"""
功能：构建一个访问记录的向量模型
输入：action，用户的一个方位记录，dict，字段同数据库
返回：向量模型，list，元素为[特征id，特征值]
"""


def get_vsm(action):
    uid = action["uid"]
    vid = action["source_vid"]
    # 获得用户信息
    user_info = get_user_info(uid)

    # 获得视频信息
    video_info = get_video_info(vid)
    if not video_info:
        return -1

    # 获得场景信息
    scene_info = get_scene_info(action, user_info, video_info)

    # 构建特征向量
    vsm = []  # 特征向量，内容为[特征id，特征值]
    # 处理用户关键词特征，包含的值都为1
    user_keyword_list = user_info["appbk_tags"].split(",")
    for word in user_keyword_list:
        feature_name = ("uw_" + word)
        if feature_name in feature_name_id_dict:
            feature_id = feature_name_id_dict[feature_name]
            vsm.append([feature_id, 1])

    # 处理用户类别特征
    user_category_list = user_info["appbk_sub_category"].split(",")
    for category in user_category_list:
        feature_name = ("uc_" + category)
        if feature_name in feature_name_id_dict:
            feature_id = feature_name_id_dict[feature_name]
            vsm.append([feature_id, 1])

    # 处理视频关键词特征
    video_keyword_list = video_info["appbk_tags"].split(",")
    for word in video_keyword_list:
        feature_name = ("vw_" + word)
        if feature_name in feature_name_id_dict:
            feature_id = feature_name_id_dict[feature_name]
            vsm.append([feature_id, 1])

    # 处理视频的类别特征
    video_category_list = video_info["appbk_sub_category"].split(",")
    for category in video_category_list:
        feature_name = ("vc_" + category)
        if feature_name in feature_name_id_dict:
            feature_id = feature_name_id_dict[feature_name]
            vsm.append([feature_id, 1])

    # 视频来源
    source = video_info["source"]
    feature_name = "s_" + source
    feature_id = feature_name_id_dict[feature_name]
    vsm.append([feature_id, 1])

    # 视频时长id
    duration = video_info["duration"]
    feature_name = "duration_second"
    feature_id = feature_name_id_dict[feature_name]
    vsm.append([feature_id, duration])

    # 视频标题长度
    title_length = video_info["title_length"]
    feature_name = "title_length"
    feature_id = feature_name_id_dict[feature_name]
    vsm.append([feature_id, title_length])

    # 用户关键词和视频关键词重复数
    keyword_match = scene_info["keyword_match"]
    feature_name = "keyword_match"
    feature_id = feature_name_id_dict[feature_name]
    vsm.append([feature_id, keyword_match])

    # 获得用户类别和视频类别重复数
    category_match = scene_info["category_match"]
    feature_name = "category_match"
    feature_id = feature_name_id_dict[feature_name]
    vsm.append([feature_id, category_match])

    # 获得用户浏览视频的时间点
    view_hour = scene_info["hour"]
    feature_name = "hour_" + str(view_hour)
    feature_id = feature_name_id_dict[feature_name]
    vsm.append([feature_id, 1])

    return vsm


"""
功能：构建正例子的特征
"""


def build_view_action():
    action_list = get_user_actions()
    action_id_list = []  # 记录有效的action id
    for action in action_list:
        # print action
        vsm = get_vsm(action)
        if -1 == vsm:
            continue
        action_id_list.append(action["id"])  # 记录有效的action id

        feature_id_value_list = sorted(vsm, key=lambda d: d[0], reverse=False)

        # step 4, 输出
        vsm_item_list = []
        for (key, value) in feature_id_value_list:
            vsm_item_list.append([key, value])

        vsm_str_list = []
        for item in vsm_item_list:
            feature = str(item[0]) + ":" + str(item[1])
            if feature not in vsm_str_list:
                vsm_str_list.append(feature)

        print("1" + " " + " ".join(vsm_str_list))


"""
功能：根据action，构建一个反例
"""


def build_unview(action):
    vid = action["source_vid"]  # 视频id
    uid = action["uid"]  # 用户id
    linux_time = time.mktime(action["update_time"].timetuple())
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(linux_time))
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(linux_time - 7 * 24 * 60 * 60))

    # 默认推荐的为最近7天的记录，随机抽取一个
    sql = "select id from video_info_ctr where down_action_time>='" + start_time + "' and down_action_time<='" + end_time + "' and  id not in " \
          + "(select source_vid from user_action_ctr where uid='" + uid + "') order by rand() limit 1"
    result = sql_appbk.mysql_com(sql)
    if result:
        action["source_vid"] = result[0]["id"]
        return action
    else:
        return -1


"""
功能：构建负例的特征
"""


def build_unview_action():
    action_list = get_user_actions()

    for action in action_list:
        # print action
        action = build_unview(action)
        if -1 == action:
            continue

        vsm = get_vsm(action)
        if -1 == vsm:
            continue

        feature_id_value_list = sorted(vsm, key=lambda d: d[0], reverse=False)

        # step 4, 输出
        vsm_item_list = []
        for (key, value) in feature_id_value_list:
            vsm_item_list.append([key, value])

        vsm_str_list = []
        for item in vsm_item_list:
            feature = str(item[0]) + ":" + str(item[1])
            if feature not in vsm_str_list:
                vsm_str_list.append(feature)

        print("-1" + " " + " ".join(vsm_str_list))


if __name__ == "__main__":
    load_feature_id()
    # print feature_name_id_dict["uw_爆笑"]
    build_view_action()
    build_unview_action()
