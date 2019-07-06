#!/bin/sh
#########################################################################
# Author: 
# Created Time: Mon 29 Oct 2018 09:32:29 AM CST
# File Name: get_item_based_control.sh
# Description:基于物品的推荐 
#########################################################################
#step 1,获得相似的物品列表
./get_similar_item_3.py  > similiar_item.json

#一个降低计算复杂度的实现,供参考
#./process.sh

#step 2,插入数据库,耗时较长
./insert_sql.py similiar_item.json item_based_rec
#使用load插入,请自行修改第一步输出格式
#./load_item.sh similiar_item.tab

#step 3,测试一个结果
./get_item_based_rec_3.py
