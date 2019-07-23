#!/usr/bin/env python
# coding=utf-8
import sys
import os
import hashlib
import json
import re
import get_vsm  # 获得向量模型
from sklearn.svm.libsvm import predict

sys.path.append('/root/bigdata/develop_kit/liblinear-2.30/python')
from liblinear import *
from liblinearutil import *

model_ = ''  # liblinear模型
classes_dict = {}


# 加载类别
def load_classes(filename="category.dat"):
    classes_file = open(filename, "r")
    for line in classes_file:
        line = line.strip()
        item_list = line.split()
        id = item_list[0]  # 类别id
        name = item_list[1]  # 类别名
        classes_dict[id] = name


# 获得概率最高的3个类别
def get_max_prob_classes(prob_list, top_n=3):
    # 获得类别标签,该标签顺序如预测标签概率顺序一致
    label_list = model_.get_labels()
    prob_list_sort = sorted(prob_list, reverse=True)  # 从大到小排序
    # 找出最大的top n概率的index,利用index找到类别标签
    classes_list = []
    for prob in prob_list_sort[0:top_n]:
        index = prob_list.index(prob)
        label = str(label_list[index])  # 类别id
        name = classes_dict[label]  # 类别名称

        classes_list.append(name)
    return classes_list


# 分类
def classify(line):
    word_id_list = get_vsm.get_vsm(line)
    tmp_dict = {}  # 临时词典,key为特征id,value为特征值

    if len(word_id_list) > 0:
        for item in word_id_list:
            tmp_dict[item[0]] = item[1]

        y = []
        x = []
        x.append(tmp_dict)
        # liblinear python接口
        p_labs, p_acc, p_vals = predict(y, x, model_, '-b 1')
        print(p_labs,p_vals)
        return get_max_prob_classes(p_vals[0])
    else:
        return -1


# jieba.disable_parallel() #禁用多进程
get_vsm.load_word_dict("idf.dict")
load_classes()  # 加载类别
# model_ = load_model("iqiyi_1.train.vsm.model")  # 加载模型
model_ = load_model("iqiyi_1.train.vsm.model")  # 加载模型
# 处理每一行
"""
for line in sys.stdin:
    line = line.strip()
    classify(line)
"""
if __name__ == "__main__":
    line = "明星荧幕初吻大曝光"
    # classify(line)
    print(json.dumps(classify(line), ensure_ascii=False))
