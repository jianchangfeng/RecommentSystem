#!/usr/bin/env python3
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Sep 2018 12:00:24 PM CST
# File Name: user_based_offline_3.py
# Description: 
######################################################################
import json
import time
import sys
from math import sqrt

"""
功能:计算两个用户的余弦距离
输入: person1, 用户1的点击记录,dict,key为视频id,value=1
输入: person2, 用户2的点击记录,dict,key为视频id,value=1
返回: 余弦相似度
"""


def cos_distance(person1, person2):
    dot_sum = 0
    for item in person1:
        if item in person2:
            dot_sum += person1[item] * person2[item]
    if 0 == len(person1) or 0 == len(person2):
        return 0
    else:
        score = float(dot_sum) / sqrt(len(person1) * len(person2) * 1.0)  # 向量元素值均为1
        return score


"""
功能:加载用户行为数据
输入:用户行为数据文件名,数据格式为 uid + \t + vid 
返回:用户行为数据,dict,key为uid,value也为dict( key为vid, value=1)
"""


def load_action_data(filename="action.dat"):
    action_data = {}
    data_file = open(filename, "r")
    for line in data_file:
        line = line.strip()
        item_list = line.split("\t")
        uid = item_list[0]
        vid = item_list[1]
        action_data.setdefault(uid, {})
        action_data[uid][vid] = 1
    # print (action_data)
    return action_data


"""
功能: 为一个用户推荐视频
输入:action_data, 用户行为数据
输入:uid, 用户id
返回: 为用户推荐的视频列表
"""


def get_recommend(action_data, uid, sim=cos_distance):
    score_sum = {}  # 记录视频的推荐得分,key为vid,value为对应的得分加和
    # sim_sum = {} #记录一个视频的相似度加和,key为vid,value为对应相似度加和

    uid_action = action_data[uid]  # 推荐用户的点击记录

    # 遍历每一个用户,对相似的用户,获得推荐
    for other_uid in action_data:
        if uid == other_uid:  # 自己的不计算
            continue

        other_action = action_data[other_uid]  # 其他用户的行为数据
        sim_score = sim(uid_action, other_action)

        if 0 == sim_score:  # 如果没有任何相似,则不进行推荐
            continue

        # 对相似的用户,获得其浏览记录,以及对应的推荐得分
        for vid in other_action:
            if not vid in uid_action:  # 用户已经看过的视频不计算
                score_sum.setdefault(vid, 0)
                score_sum[vid] += sim_score * other_action[vid]  # 相似用户对该视频的推荐分

    # 获得最终的得分
    recommend_list = []
    for vid in score_sum:
        # final_score = float(score_sum[vid])/sim_sum[vid]
        final_score = score_sum[vid]
        recommend_list.append((vid, final_score))

    final_recommend_list = sorted(recommend_list, key=lambda d: d[1], reverse=True)  # 按照第二个关键字来排序，降序
    return final_recommend_list


"""
功能:获得所有用户的推荐列表
输入:filename, 用户行为数据文件名
输入: max_num, 为一个用户最多推荐多少条
返回:
"""


def get_all_recommend(filename="action.dat", max_num=50):
    # step 1, 加载用户行为数据
    action_data = load_action_data()

    # step 2, 获得所有用户的推荐,每个用户最多推荐max_num个视频
    for uid in action_data:
        print(uid)
        vid_score_list = get_recommend(action_data, uid)  # 推荐的视频vid列表
        vid_list = []
        for vid, score in vid_score_list:
            vid_list.append(vid)
        recommend = {}
        recommend["uid"] = uid
        recommend["vid"] = ",".join(vid_list[0:max_num])
        print(json.dumps(recommend))
    return 0


if __name__ == "__main__":
    # 获得所有用户的推荐结果
    get_all_recommend()
    # 测试一个推荐结果
    """
    action_data = load_action_data()
    uid = "1"
    recommend = get_recommend(action_data, uid)
    print (recommend[0:10])
    """
