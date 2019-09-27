#!/bin/sh
#########################################################################
# Author: 
# Created Time: Mon 29 Oct 2018 08:55:23 AM CST
# File Name: build_action_control.sh
# Description:根据标准数据集,映射实验数据集 
#########################################################################
#step 1, 构建数据集,修改 build_action输出的数据格式,分别测试插入数据库的速度
#./build_action_3.py u.data > u.data.json
./build_action_3.py u.data > u.data.tab

#step 2,插入数据库
#./insert_sql.py  u.data.json user_action
./load_action.sh u.data.tab
