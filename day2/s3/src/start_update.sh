#!/bin/sh
#########################################################################
# Author: billczhang
# Created Time: Mon 15 Oct 2018 09:27:56 PM CST
# File Name: start_update.sh
# Description: 循环执行更新程序
#########################################################################
set -x
while [ 1 ]
do
    #更新
    ./update_user_model_control.sh >> update_user_model_control.log 
    sleep 10
done
