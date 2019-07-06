#!/usr/bin/env python
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 04 Jul 2017 05:30:57 PM CST
# File Name: get_tag.py
# Description: 获得关键词标签
######################################################################
import json
import time
import sys
import jieba
import jieba.posseg as pseg
import jieba.analyse

"""
功能：获得一个文本的关键词标签
输入：text，一个文本
返回：文本的标签列表，list
"""
def get_tags(text):
    #获得过tag
    word_list = jieba.analyse.extract_tags(text, 3,allowPOS=['ns', 'n', 'vn', 'v', 'nr', 'x']) #tf*if
    #word_list = jieba.analyse.textrank(text, 3,allowPOS=['ns', 'n', 'vn', 'v', 'nr', 'x']) #word rank
    # " ".join(word_list)
    return word_list

    

if __name__=='__main__':
    line = "线程是程序执行时的最小单位，它是进程的一个执行流"
    print(get_tags(line))
