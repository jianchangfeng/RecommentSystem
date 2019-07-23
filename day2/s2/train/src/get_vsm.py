#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 04 Jul 2017 05:30:57 PM CST
# File Name: get_svm.py
# Description: 
######################################################################
import json
import time
import sys
import jieba
import jieba.posseg as pseg
import jieba.analyse

# 记录word的id
word_id_dict = {}

# 记录word的idf
word_idf_dict = {}

"""
功能：加载词的id 和 idf
输入：idf文件名
输出：无
返回：0正确，1错误
"""


def load_word_dict(filename):
    input_file = open(filename, 'r')

    word_id = 1
    for line in input_file:
        line = line.strip()
        item_list = line.split()
        word = item_list[0]
        try:
            idf = float(item_list[1])
        except:
            continue
            # print(line)
        word_idf_dict[word] = idf

        word_id_dict[word] = word_id
        word_id += 1
    return 0


"""
功能：分词,进行词性过滤
输入：一个文本
输出：无
返回：分词list
"""


def get_seg(line):
    # d = line.split()
    # d = jieba.lcut(line)
    d = pseg.cut(line)
    word_list = []
    for item in d:
        # 词性过滤
        if item.flag != "x" and item.flag != "uj" and \
                item.flag != "m" and item.flag != "p" and item.flag != "y" and \
                item.flag != "u":
            word = item.word  # python3
            # word = item.word.encode("utf-8", "ignore") #python2
            # print word
            word_list.append(word)
    return word_list


def get_vsm(text):
    # step 1,分词
    word_list = get_seg(text)

    # step 2, 统计tf
    word_tf_dict = {}
    for word in word_list:
        if word == "":
            continue
        word_tf_dict.setdefault(word, 0)
        word_tf_dict[word] += 1

    # step 3， 计算tf*idf,key=word_id, value=tf*idf
    word_id_value_dict = {}
    for word in word_tf_dict:
        if word in word_id_dict:
            word_id = word_id_dict[word]
            word_id_value_dict[word_id] = word_tf_dict[word] * word_idf_dict[word]
        else:
            # print("ERROR ",word)
            continue
    # 按照word id排序,python3 是items, python2是iteritems
    word_id_value_list = sorted(word_id_value_dict.items(), key=lambda d: d[0], reverse=False)

    # step 4, 输出
    vsm_item_list = []
    for (key, value) in word_id_value_list:
        vsm_item_list.append([key, value])
        # vsm_item_list.append( str(key) + ":" + str(value) )

    # return " ".join(vsm_item_list)
    return vsm_item_list


def process_corpus(data_file):
    input_data_file = open(data_file, 'r')

    for line in input_data_file:
        line = line.strip()
        # print(line)
        line_list = line.split(" ")  # 空格分开
        # print(line_list)
        if len(line_list) >= 2:
            category_id = line_list[0]
            text = line_list[1]
        else:
            # print("ERROR")
            continue

        vsm = get_vsm(text)
        vsm_str_list = []
        for item in vsm:
            vsm_str_list.append(str(item[0]) + ":" + str(item[1]))

        print(category_id + " " + " ".join(vsm_str_list))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("please input dict file and data file name")
        sys.exit()

    dict_file = sys.argv[1]  # idf字典
    load_word_dict(dict_file)
    data_file = sys.argv[2]  # 语料
    # 处理语料,生成vsm输入数据
    process_corpus(data_file)
