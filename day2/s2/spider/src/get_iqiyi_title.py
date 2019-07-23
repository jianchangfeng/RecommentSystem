#!/usr/bin/python
# coding=utf-8
import sys
import time

from io import StringIO
import importlib
import socket
importlib.reload(sys)
socket.setdefaulttimeout(120)
import json
from bs4 import BeautifulSoup
import gzip
import urllib3
import urllib
from urllib.parse import quote
import string



def download_url(url):
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'host': "www.baidu.com",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }
    # cookie = cookielib.CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    # request = urllib2.Request(url)
    #
    # request.add_header('Upgrade-Insecure-Requests','1')
    # request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
    # request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    # request.add_header('Accept-Encoding','gzip,deflate,sdch')
    # request.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6')

    # request.add_header('Cookie','YF-Page-G0=cf25a00b541269674d0feadd72dce35f;SUB=_2AkMvo4Pnf8NxqwJRmPkSzWrkboh1zA_EieKZ_3I8JRMxHRl-yT83qmVbtRALpE9rPnLvt9uromtQupHbRsotJQ..;SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WW3pjG-LAAZ0gdZKQl7rCIX;YF-V5-G0=d22a701aae075ca04c11f0ef68835839;_s_tentry=-;Apache=1881909054980.5928.1493119016368;SINAGLOBAL=1881909054980.5928.1493119016368;ULV=1493119016441:1:1:1:1881909054980.5928.1493119016368:;WBStorage=02e13baf68409715|undefined')

    result = {}
    # print request
    try:
        url = quote(url, safe=string.printable)
        response = urllib.request.urlopen(url)
        # http = urllib3.PoolManager()
        # r = http.request('GET', url, headers=headers)
        # response = r.getresponse()
        # print(response)

        # response = urllib2.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            text = f.read()
        else:
            text = response.read()
        response.close()
        if len(text) > 1000:
            result['status'] = 0
            result['text'] = text
            # result = json.loads(text)
        else:
            result['status'] = 1
            error_info = 'Error:text too short'
            result['text'] = error_info
    except Exception as e:
        result['status'] = 1
        result['text'] = 'Error:' + str(e)
        return result
    return result


def assemble_html_iqiyi_data(html, category_info=""):
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find('ul', {"class": "qy-mod-ul"})
    # print(ul)
    if ul:
        alist = ul.find_all('li')
    else:
        return -1
    # print "alist:"+str(alist)
    sqldata = {}
    for anode in alist:
        # print("anode:"+str(anode))
        # href = anode['href']
        # div = anode.find('div',{"class:":"site-piclist_info"})
        # div = anode.find('div', {"class:": "site-piclist_pic"})
        # print(anode)
        p = anode.find('p', {"class": "main"})
        ainfo = p.find('a')
        vid = ainfo['href'][21:33]
        sqldata['vid'] = vid
        sqldata['title'] = ainfo['title']
        # sqldata['link'] = ainfo['href']
        sqldata['link'] = category_info['category_url']
        sqldata['source'] = "iqiyi"
        sqldata['category'] = category_info['category_name']
        sqldata['appbk_category'] = '搞笑'
        sqldata['fetch_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print "vid"+vid
        # print "ainfo:"+str(ainfo)
        # print str(div['href'])
        print(json.dumps(sqldata))


def next_url(url, i):
    new_url = url[:-17] + str(i) + url[-16:]
    return new_url


if __name__ == "__main__":
    category_info_list = [
        {"category_name": "欢乐精选",
         "category_url": "http://list.iqiyi.com/www/22/22169-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "娱乐八卦",
         "category_url": "http://list.iqiyi.com/www/22/29115-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "搞笑短片",
         "category_url": "http://list.iqiyi.com/www/22/29116-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "影视剧吐槽",
         "category_url": "http://list.iqiyi.com/www/22/29139-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "雷人囧事",
         "category_url": "http://list.iqiyi.com/www/22/22172-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "爆笑节目",
         "category_url": "http://list.iqiyi.com/www/22/22171-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "萌宠", "category_url": "http://list.iqiyi.com/www/22/1905-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "童趣", "category_url": "http://list.iqiyi.com/www/22/1909-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "奇闻趣事", "category_url": "http://list.iqiyi.com/www/22/1900-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "恶搞配音", "category_url": "http://list.iqiyi.com/www/22/1902-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "相声", "category_url": "http://list.iqiyi.com/www/22/1903-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "小品", "category_url": "http://list.iqiyi.com/www/22/1904-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "猎奇", "category_url": "http://list.iqiyi.com/www/22/22170-------------11-1-2-iqiyi-1-.html"},
        {"category_name": "啪啪奇", "category_url": "http://list.iqiyi.com/www/22/2327-------------11-1-2-iqiyi-1-.html"}
    ]
    for item in category_info_list:
        for i in range(1, 31):

            new_url = next_url(item['category_url'], i)
            # print(new_url)
            res = download_url(new_url)
            if (res['status'] == 0):
                html = res['text']
                # print(html)
                assemble_html_iqiyi_data(html, item)
