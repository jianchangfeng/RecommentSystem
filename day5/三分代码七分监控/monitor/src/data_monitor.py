#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 11 Jul 2017 04:29:27 PM CST
# File Name: data_monitor.py
# Description:mysql数据监控
######################################################################
import json
import time
import sys
import configparser
import sql_appbk

"""
功能：执行监控sql语句，错误报警
输入：config，配置文件，包含监控用sql语句
返回：
"""
def get_data(config="../conf/data_monitor.conf"):
    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read(config)

    #读取sections
    section_list = cf.sections()

    #依次读取section的每一个内容
    for section in section_list:
        sql = cf.get(section, "sql") #sql语句
        min_num = cf.getint(section, "min_num") #获得最小值
        #执行sql语句

        result = sql_appbk.mysql_com(sql)
        num = result[0]["num"]
        if num<min_num:
            #调用短信报警代码，进行报警
            print("Error：数据 " + section)

if __name__=="__main__":
    get_data()
