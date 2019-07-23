#!/bin/sh
#########################################################################
# Author: 
# Created Time: Wed 17 Oct 2018 06:57:52 PM CST
# File Name: get_vsm_control.sh
# Description: 获得向量空间模型
#########################################################################
#测试idf程序
cat 1.txt|./get_idf_cn.py

#step 1,获得向量空间模型
./get_vsm.py idf.dict train.dat > train.dat.vsm
