#!/usr/bin/env python
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Fri 14 Jul 2017 12:09:52 PM CST
# File Name: get_similar_item.py
# Description: 获得物品的相似物品
######################################################################
import json
import time
import sys
from math import sqrt
reload(sys)
sys.setdefaultencoding('utf8')

#求皮尔逊相关系数
def sim_pearson(p1,p2):
    #得到双方都曾评价过的物品列表
    si={}
    for item in p1:
        if item in p2:
            si[item]=1

    n = len(si)
    if n ==0:
        return 0

    #对所有偏好求和
    sum1 = sum(p1[it] for it in si)
    sum2 = sum(p2[it] for it in si)

    #求平方和
    sum1sq = sum(pow(p1[it],2) for it in si)
    sum2sq = sum(pow(p2[it], 2) for it in si)

    #求乘积之和
    pSum = sum(p1[it]*p2[it] for it in si)

    #计算皮尔逊评价值
    num =pSum-(sum1*sum2/n)
    den = sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den == 0:
        return 0
    r = num/den
    return r

"""
功能:计算的余弦距离
输入: item1, dict,key为特征id,value=1
输入: item2, dict,key为特征id,value=1
返回: 余弦相似度
"""
def cos_distance(item1,item2):
    dot_sum = 0
    for item in item1:
        if item2.has_key(item):
            dot_sum += item1[item]*item2[item]
    if 0==len(item1) or 0==len(item2):
        return 0
    else:
        score = float(dot_sum)/sqrt( len(item1)* len(item2) * 1.0 ) #向量元素值均为1
        return score

"""
功能:加载用户行为数据
输入:用户行为数据文件名,数据格式为 uid + \t + vid 
返回:用户行为数据,dict,key为vid,value也为dict( key为uid, value=1)
"""
def load_action_data(filename="action.dat"):
    action_data = {}
    data_file = open(filename,"r")
    for line in data_file:
        line = line.strip()
        item_list = line.split("\t")
        uid = item_list[0]
        vid = item_list[1]
        action_data.setdefault(vid,{})
        action_data[vid][uid] = 1
    return action_data


"""
功能: 获得一个视频的相似视频
输入:action_data, 用户行为数据
输入:vid, 视频id
返回: 输出热度相似度最高的视频列表
"""

def get_sim_item(action_data, vid, sim=cos_distance,top=10):
    sim_video_list = []  # 记录视频的相似视频,内容为元组(vid视频id，sim相似度)

    vid_vsm = action_data[vid]  #视频的用户向量表示

    # 遍历每一个视频，获得相似度
    for other_vid in action_data:
        if vid == other_vid:  # 自己的不计算
            continue

        other_vid_vsm = action_data[other_vid]  # 其他视频的向量表示
        sim_score = sim(vid_vsm, other_vid_vsm) #求相似度
        sim_video_list.append([other_vid,sim_score])


    final_sim_list = sorted(sim_video_list, key=lambda d: d[1], reverse=True)
    #打印输出
    for vid2,score in final_sim_list[0:top]:
        sim_data = {}
        sim_data["vid1"] = vid
        sim_data["vid2"] = vid2
        sim_data["sim"] = score
        if int(vid)<int(vid2): #相似度只记录一遍即可
            print json.dumps(sim_data)
            #print str(vid) + "\t" + str(vid2) + "\t" + str(score)

"""
功能:获得所有视频的相似视频
输入:filename, 用户行为数据文件名
输入: max_num, 一个视频最多的相似视频数
返回:
"""
def get_all_sim_item(filename="action.dat", max_num=10):
    #step 1, 加载用户行为数据
    action_data = load_action_data()

    #step 2, 获得所有视频的相似视频,最多max_num个视频
    for vid in action_data:
        get_sim_item(action_data, vid)

if __name__=="__main__":
    get_all_sim_item()
