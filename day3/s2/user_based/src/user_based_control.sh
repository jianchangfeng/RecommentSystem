#!/bin/sh
#########################################################################
# Author: billczhang
# Created Time: Mon 29 Oct 2018 09:11:22 AM CST
# File Name: user_based_control.sh
# Description: 基于用户的推荐
#########################################################################
#step 1,获得点击行为数据
./get_action_data_3.py > action.dat

#step 2,获得基于用户的推荐结果
./user_based_offline_3.py > user_based.json

#step 3,插入数据库
./insert_sql.py user_based.json user_based_rec

#step 4,测试一个推荐结果
./get_user_based_rec_3.py 
