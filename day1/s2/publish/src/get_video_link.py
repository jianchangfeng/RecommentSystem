#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @youyue-inc.com
# Created Time: May 18  2017 18:55:41 PM CST
# File Name:get_video_link.py 
# Description:获得每个机器需要下载的视频链接,通过ip分配下载任务
# 输入为 ip.conf配置文件,记录每个机器的ip
# 输出为 视频链接 + "\t" + 文件名 的形式,文件名不包含视频格式扩展名
#########################################################################
import os
import sys
import time
import json
import urllib
import configparser
import logging
import socket
import fcntl
import struct
import sql_appbk

# reload(sys)
# sys.setdefaultencoding('utf-8')

"""
功能:获取本地ip
输入:ifname, 网卡名称
返回: 本机ip地址,目前使用外网地址
"""


def get_ip_address(ifname="eth1"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


"""
功能:获取本机任务分配信息,根据ip划分任务
输入:配置文件
返回: 本机的任务任务信息,dict: len为任务总数,index为本机领取的取余数
"""


def get_job_info(conf_file_name="ip.conf"):
    cf = configparser.ConfigParser.ConfigParser()
    cf.read(conf_file_name)
    ip_list = []  # 所有ip列表
    for key in cf.options("ip_list"):
        ip_list.append(cf.get("ip_list", key))

    localip = get_ip_address()  # 本机ip

    ipinfo = {}  # ip信息
    ipinfo['len'] = len(ip_list)  # 总长度
    if localip in ip_list:
        ipinfo['index'] = ip_list.index(localip)  # 本机ip的index
    else:
        ipinfo['index'] = 0
    return ipinfo


"""
功能:获得本机分配的视频下载链接任务信息
输入:无
输出:打印输出,视频link,下载文件名
"""


def get_video_link():
    # job_info = get_job_info()
    # 获得未下载的视频链接,根据id取模,获得本机需要下载的link信息,取3天内的
    # sql_com = "select id,vid,link,source FROM video_info_test where DATEDIFF(NOW(),fetch_time)<3 and duration <301 and (public_type='all' or public_type is null) and (id%"+str(job_info['len'])+")="+str(job_info['index'])+" and down_action_time IS NULL"
    sql_com = "select id,vid,link,source FROM video_info where DATEDIFF(NOW(),fetch_time)<10 and duration <301 and (public_type='all' or public_type is null) and is_download=0"
    result = sql_appbk.mysql_com(sql_com)
    for row in result:
        filename = row["source"] + "_" + row["vid"]
        print(row["link"] + "\t" + filename)


if __name__ == "__main__":
    get_video_link()
