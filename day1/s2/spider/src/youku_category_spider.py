#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @youyue-inc.com
# Created Time: Wed 19 Apr 2017 02:55:41 PM CST
# File Name: youku_category_spider.py
# Description:根据类别，下载youku的数据
# 下载并落地json文件
#########################################################################
import os
import sys
import time
import json
import configparser
# import ConfigParser #python 2
import logging
import socket
import urllib
import urllib.parse
import urllib.request

# import urllib2 #python2
# reload(sys) #python2
# sys.setdefaultencoding('utf-8') #python2
socket.setdefaulttimeout(60)

log_filename = "../log/youku_category_spider.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

"""
功能：获得一个client id,可以多申请几个，每次随机取一个，增加下载量
输入：无
返回：client_id
"""


def get_client_id():
    client_id = "76e0d8ab091b3e02"
    return client_id


"""
功能：从api接口下载数据
输入：category, 一级类别
输入: appbk_cateory, appbk对应的类别
返回：无
"""


def get_youku_video(category, appbk_category):
    # 通过类别获得信息,http://doc.open.youku.com/?docid=330
    url = "https://openapi.youku.com/v2/videos/by_category.json"

    # 获得一个client id
    client_id = get_client_id()

    # 参数
    # params = urllib.urlencode( #python2
    params = urllib.parse.urlencode(
        {'client_id': client_id,
         'category': category,
         'period': 'week',  # 时间范围 today: 今日 week: 本周 month: 本月 history: 历史
         'orderby': 'view-count',
         # 排序方式,排序 published: 发布时间 view-count: 总播放数 comment-count: 总评论数 reference-count: 总引用 favorite-time: 收藏时间
         # favorite-count: 总收藏数
         'page': '1',  # 页码，默认第一页，后续可翻页
         'count': '100'  # 每页面的数据数
         })
    url = url + "?" + params
    print(url)
    try:
        # json_content = urllib.urlopen(url).read() #python2
        json_content = urllib.request.urlopen(url).read().decode('utf-8')
        results = json.loads(json_content)
        print_json(results, appbk_category)
    except Exception as e:
        # print(e)
        logging.info(e)
    #        sys.exit(1)


"""
功能：打印json数据
输入：结果数组
返回：
"""


def print_json(results, appbk_category):
    videos = results["videos"]
    for video in videos:
        video["vid"] = video["id"]  # 视频id
        video["username"] = video["user"]["name"]  # 改写name字段
        video["userid"] = video["user"]["id"]  # 改写user id字段
        video["userlink"] = video["user"]["link"]  # 改写user字段
        video["operation_limit"] = ",".join(video["operation_limit"])
        video["streamtypes"] = ",".join(video["streamtypes"])
        video["fetch_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 下载时间
        video["source"] = "youku"  # 来源
        video["appbk_category"] = appbk_category  # appbk内部类别
        del video['user'];
        del video["id"]
        del video["day_vv"]
        print(json.dumps(video))


if __name__ == "__main__":
    # get_youku_video("搞笑", "搞笑")
    # for line in sys.stdin:
    #     line = line.strip()
    #     item_list = line.split(" ")
    #     category = item_list[0]
    #     appbk_categroy = item_list[1]
    #     get_youku_video(category, appbk_categroy)
    with open('category.dat', 'r', encoding='UTF-8') as f:
        for line in f:
            print(line)
            item_list = line.split(" ")
            category = item_list[0]
            appbk_categroy = item_list[1]
            get_youku_video(category, appbk_categroy)
