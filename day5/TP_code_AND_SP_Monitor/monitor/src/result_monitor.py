#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Tue 11 Jul 2017 04:29:27 PM CST
# File Name: result_monitor.py
# Description:推荐结果监控
######################################################################
import json
import time
import sys
import urllib
import urllib.parse
import urllib.request
import socket
socket.setdefaulttimeout(120)


"""
功能：返回api的结果
输入：method，方法名
输入：data，请求数据，dict结构
返回：结果文本
"""
def get_result(method, data):
    # step 1，获得搜索结果html页面
    params = urllib.parse.urlencode(data)
    host = "http://localhost:8080/" #填写你的host
    url = host + method + "?" + params
    text = urllib.request.urlopen(url).read().decode('utf-8')
    return text

#获得数据
def get_report(method,data):
    try:
        ret = get_result(method, data)
        result = json.loads(ret)
        status = result["status"]
        result_num = len(result["results"])
        if 0!=int(status):
            print("Error:服务状态错误")
            #报警

        if 10!=result_num:
            print("Error:推荐结果错误")

    except Exception as e:
        print ("Error：服务出错",e)
        #短信报警
        return -1
    print("服务器状态正确")
    return 0


if __name__=="__main__":
    method = "get_videos_by_category"
    data = {"c":"搞笑"}
    get_report(method,data)
