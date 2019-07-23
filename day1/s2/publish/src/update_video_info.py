#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @youyue-inc.com
# Created Time: May 18  2017 18:55:41 PM CST
# File Name:get_video_link.py 
# Description:根据下载的文件名,更新数据库信息
# 输入为 path/source_vid.mp4的格式,解析出source和vid后,更新对应的数据记录,表示已经下载
# 输出为 更新数据库
#########################################################################
import os
import sys
import time
import json
import urllib
import configparser
import logging
import sql_appbk

# reload(sys)
# sys.setdefaultencoding('utf-8')

"""
功能:根据视频文件名,更新数据库,如path/source_vid.mp4
输入:视频文件名,可能带路径
输出:
"""


def update_video_info(filename):
    video_file = filename.split("/")[-1]  # 去掉可能包含的路径
    video_file = video_file.split(".")[0]  # 去掉可能的扩展名
    item_list = video_file.split('_')
    source = item_list[0]
    vid = item_list[1]
    down_action_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql_com = "update video_info set down_action_time='" + down_action_time + "',is_download=1 where source='" + str(
        source) + "' and vid='" + str(vid) + "'"
    ret = sql_appbk.mysql_com(sql_com)
    return ret


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please input filename")
        sys.exit()
    filename = sys.argv[1]
    update_video_info(filename)
