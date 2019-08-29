#!/usr/bin/env python
#coding=utf-8
import sys
import os
import math
import json
from math import sqrt
#reload(sys)
#sys.setdefaultencoding('utf8')

"""
功能:加载用户行为数据
输入:用户行为数据文件名,数据格式为 uid + \t + vid 
返回:用户行为数据,dict,key为vid,value为访问过vid的用户数
"""
def load_action_data(filename="./action.dat"):
    action_data = {}
    data_file = open(filename,"r")
    for line in data_file:
        line = line.strip()
        item_list = line.split("\t")
        uid = item_list[0]
        vid = item_list[1]
        action_data.setdefault(vid,0)
        action_data[vid] += 1
    return action_data

ACTION_DATA = load_action_data() #全局变量

current_key = None
current_value_list = []

#处理一个视频和另一个视频的相似度
def process_value_list(key, value_list):
    sim = sum(value_list) #相似度
    sim_data = {}
    (sim_data["vid1"], sim_data["vid2"]) = key.split("|")
    sim_data["sim"] = float(sim)/sqrt(  ACTION_DATA[sim_data["vid1"]]*ACTION_DATA[sim_data["vid2"]]* 1.0 )  #相似度
    if sim>0.3:#只输出相似度较高的
        #print json.dumps(sim_data)
        print(sim_data["vid1"] + "\t" + sim_data["vid2"] + "\t" + str(sim_data["sim"]))


for line in sys.stdin:
    line = line.strip()
    (key,value) = line.split("\t")
    value = float(value)
    if current_key == key:#如果词没有变，则累加
        current_value_list.append(value)
    else:#如果词发生变化了,则输出
        if current_key != None:
            #如果读的是第一行，和 None不一致,但不输出，不是第一行才输出
            process_value_list(current_key, current_value_list)
        #初始化
        current_key = key
        current_value_list = []
        current_value_list.append(value)

#最后一行处理，如果是和前面一样的词，后续没有词了，则前面没有输出
if current_key:
    process_value_list(current_key, current_value_list)
