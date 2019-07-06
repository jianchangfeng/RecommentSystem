#!/usr/bin/env python
#coding=utf-8
import sys
import os
sys.path.append("./jieba")
import jieba
import re
#importlib.reload(sys)


#统计语料的idf


#获得关键词列表,每个词只输出一次
def get_keywords(line):
    #step 1, 删除html标签
    result = jieba.cut(line)  # 默认是精确模式
    word_dict = {}
    for word in result:
        seg = word
        if len(seg)>1:
            word_dict.setdefault(seg, 1)
    #print(word_dict) 
    for key in word_dict:
        print(key+"\t"+"1")
        
#run
#初始化分词词典
#jieba.set_dictionary('./jieba/dict.dat')
#jieba.disable_parallel() #禁用多进程

#处理每一行

for line in sys.stdin:
    line = line.strip()
    get_keywords(line)
