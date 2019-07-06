#!/usr/bin/env python
#coding=utf-8
import sys
import time
import json
from math import sqrt
import math
import jieba
import jieba.posseg as pseg
import jieba.analyse
import re

word_idf_dict = {} #记录IDF
word_df_dict = {} #记录DF
D = 0 #文档总数


#删除html标签
def del_html_tag(line):
    dr = re.compile(r'<[^>]+>',re.S)
    new_line = re.sub(dr, '', line)
    return new_line

"""
功能：分词,进行词性过滤
输入：一个文本
输出：无
返回：分词list
"""
def get_seg(line):
    #d = line.split()
    #d = jieba.lcut(line)
    d = pseg.cut(line)
    word_list = []
    for item in d:
        #词性过滤
        if item.flag!="x" and item.flag!="uj" and \
                item.flag!="m" and item.flag!="p" and item.flag!="y" and \
                item.flag!="u":
            #word = item.word.encode("utf-8", "ignore")
            word = item.word
            #print word
            word_list.append(word)
    return word_list

#获得df
def get_df(line):
    global D
    #step 1, 删除html标签
    line = del_html_tag(line)
    d = get_seg(line)

    item_distinct = del_repeat(d) #去掉重复的单词
    D = D + 1 #文档数目加1
        
    for word in d:
        word_df_dict.setdefault(word,0)
        word_df_dict[word] += 1
    return 0


#如掉重复的
def del_repeat(data_list):
    data_list = list(set(data_list))
    return  data_list

#获得idf
def get_idf():
    for key in word_df_dict:
        word_idf_dict[key] = float(D) / word_df_dict[key]
    return 0

def print_idf():
    for key in word_idf_dict:
        idf = math.log(word_idf_dict[key],2)
        if idf==0:
            idf = 0.001
        print(str(key)+"\t"+str(idf))

if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        get_df(line)
    get_idf()
    print_idf()
