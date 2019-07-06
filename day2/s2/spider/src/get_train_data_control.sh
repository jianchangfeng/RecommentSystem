#!/bin/sh
#########################################################################
# Author: billczhang
# Created Time: Wed 17 Oct 2018 04:55:55 PM CST
# File Name: get_train_data_control.sh
# Description:下载爱奇艺分类语料 
#########################################################################
set -x #调试
#step 1,下载数据
./get_iqiyi_title.py > train.json

#step 2,插入数据库
./insert_sql.py train.json video_info_iqiyi

#step 3,从数据库取数据,构建分类语料
./get_train_data.py > train.dat
