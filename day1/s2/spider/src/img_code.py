#!/usr/bin/env python27
#coding=utf-8
import sys 
import urllib2
import urllib
import re
import json
import base64
import rsa 
import binascii
from rsa import transform
import cookielib
import poster #pip install poster
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
reload(sys)
sys.setdefaultencoding('utf8')

def post_data(url, data):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 38.0.2125.101 Safari/537.36'}
    post_data = urllib.urlencode(data)   #将post消息化成可以让服务器编码的方式
    req = urllib2.Request(url, post_data, headers)
    content = urllib2.urlopen(req)
    text = content.read().decode('utf-8', 'ignore')
    return text

#获得剩余点数
def get_point():
    #url = "http://bbb4.hyslt.com/api.php?mod=php&act=point"
    url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=point"
    data = {"user_name":"maris205","user_pw":"PIN;,yin101"}
    return post_data(url, data) 

#图片识别
def get_img_result(filename):
    #url = "http://bbb4.hyslt.com/api.php?mod=php&act=upload"
    url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
    data = {"user_name":"maris205","user_pw":"PIN;,yin101",
            "yzm_minlen":"1", "yzm_maxlen":"6",
            "yzmtype_mark":"25","zztool_token":"e48de8dc1f3b7f4c28c3b3b8f7e33bc1",
            "upload":open(filename, "rb")}
    register_openers()
    datagen, headers = poster.encode.multipart_encode(data)
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request)
    text = result.read()
    json_data = json.loads(text)
    if json_data["result"]:
        return json_data["data"]["val"]
    else:
        return -1

if __name__=="__main__":
    #print get_point()
    print get_img_result("pin.png")
