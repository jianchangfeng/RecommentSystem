#!/usr/bin/env python
#coding=utf-8
import sys 
import re
import time
import json
import socket

from opensearch import const
from opensearch import Client
from opensearch import IndexApp
from opensearch import Search
from opensearch import Suggest
from config import app_key, app_secret, base_url, build_index_name, client_name

socket.setdefaulttimeout(20)

"""
功能:获得aliyun的搜索结果,为全or检索
输入:query_list, 搜索词列表,list
返回:阿里云的搜索结果
"""

def search(query_list,limit=5):
    table_name = 'main' #默认参数,不需要修改
    index_name = build_index_name
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexSearch = Search(client)
    indexSearch.addIndex("short_video") #搜索应用名称

    query_para_list = [] #检索字符串list
    for word in query_list:
        para = "default:'"+ word + "'"
        query_para_list.append(para)

    indexSearch.query = " OR ".join(query_para_list) #全or检索
    #print(indexSearch.query)
    #indexSearch.addFilter("is_download=1")

    indexSearch.start = 0 #start
    indexSearch.hits = limit #limit
    indexSearch.format = 'json' #数据结果格式
    ret = indexSearch.call()
    #print json.dumps(ret)
    return ret["result"]["items"]

if __name__=="__main__":
    query_list = ["美女","搜索"]
    print (search(query_list))

