#!/usr/bin/env python
#coding=utf-8
import sys
import os


def output(line):
    print(line + "\t"+"1")

for line in sys.stdin:
  
    #默认每一行按制表符分隔
    strs = line.strip().split("\t")#返回分隔之后的字符组成的列表
    for wd in strs:
        # 输出格式：hello   1，默认分隔符分隔的第一个元素是key，后边的都是value
        print("\t".join([wd.strip(),"1"]))
        #等价实现
        #print(wd.strip() + "\t1") 
