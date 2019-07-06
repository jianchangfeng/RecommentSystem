#!/usr/bin/env python
#coding=utf-8
import sys
import os
import math
#reload(sys)
#sys.setdefaultencoding('utf8')

current_key = None
current_value_list = []

#处理一个用户的访问记录
def process_value_list(value_list):
    for vid_left in value_list:
        for vid_right in value_list:
            if int(vid_left)<int(vid_right):
                print(vid_left+"|"+vid_right+"\t1") #两个vid共现一次,左边小,右边大


for line in sys.stdin:
    line = line.strip()
    (key,value) = line.split("\t")

    if current_key == key:#如果词没有变，则累加
        current_value_list.append(value)
    else:#如果词发生变化了,则输出
        if current_key != None:
            #如果读的是第一行，和 None不一致,但不输出，不是第一行才输出
            process_value_list(current_value_list)
        #初始化
        current_key = key
        current_value_list = []
        current_value_list.append(value)

#最后一行处理，如果是和前面一样的词，后续没有词了，则前面没有输出
if current_key:
    process_value_list(current_value_list)
