#!/bin/sh
#########################################################################
# Author: billczhang
# Created Time: Wed 17 Oct 2018 07:09:07 PM CST
# File Name: train_predict_control.sh
# Description: 训练模型
#########################################################################
#注意liblinear安装在~目录下
#liblinear的python目录需要make
#step 1,交叉验证,accuracy=53%左右
./train -s 0 -v 3 train.dat.vsm

#step 2,去掉一些重复的类别,提高精度,67%左右
grep -v "^1 " train.dat.vsm|grep  -v "^3 "|grep  -v "^13 "|grep  -v "^14 " > train_1.dat.vsm
./train -s 0 -v 3 train_1.dat.vsm

#step 3,训练模型
./train -s 0  train_1.dat.vsm #生成模型为train_1.dat.vsm.model
mv train_1.dat.vsm.model iqiyi_1.train.vsm.model

#step 4,分类测试
./get_classify.py 
