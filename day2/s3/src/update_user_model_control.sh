#!/bin/sh
#########################################################################
# Author: 
# Created Time: Mon 15 Oct 2018 08:49:39 PM CST
# File Name: update_user_model_control.sh
# Description:更新用户模型 
#########################################################################
#step1, 更新视频标签
./update_video_model.py

#step2, 更新用户模型
./update_user_model.py
