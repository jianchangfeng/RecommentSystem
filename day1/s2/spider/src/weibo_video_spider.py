#!/usr/bin/env python2
#coding=utf-8
import sys
import socket
reload(sys)
sys.setdefaultencoding('utf8')
socket.setdefaulttimeout(120)
import urllib2
import json
from bs4 import BeautifulSoup
import cookielib
import gzip
from StringIO import StringIO
import urlparse
import time
import base64
import binascii
import cookielib
import json
import os
import random
import re
import rsa
import time
import urllib
import urllib2
import urlparse
import sys
from pprint import pprint
import img_code #验证码识别


__client_js_ver__ = 'ssologin.js(v1.4.18)'

class Weibo(object):
    """"Login assist for Sina weibo."""

    def __init__(self, username, password):
        self.username = self.__encode_username(username).rstrip()
        self.password = password

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.time_str = str(int(time.time() * 100)) #linux时间字符串
        self.end_id = "" #每一页结束的微博视频id，用于请求下一页


    @staticmethod
    def __encode_username(username):
        return base64.encodestring(urllib2.quote(username))

    @staticmethod
    def __encode_password(password, info):
        key = rsa.PublicKey(int(info['pubkey'], 16), 65537)
        msg = ''.join([
            str(info['servertime']),
            '\t',
            str(info['nonce']),
            '\n',
            str(password)
        ])
        return binascii.b2a_hex(rsa.encrypt(msg, key))

    def __prelogin(self):
        url = ('http://login.sina.com.cn/sso/prelogin.php?'
               'entry=weibo&callback=sinaSSOController.preloginCallBack&rsakt=mod&checkpin=1&'
               'su={username}&_={timestamp}&client={client}'
               ).format(username=self.username, timestamp=int(time.time() * 1000), client=__client_js_ver__)

        resp = urllib2.urlopen(url).read()
        return self.__prelogin_parse(resp)

    @staticmethod
    def __prelogin_parse(resp):
        p = re.compile('preloginCallBack\((.+)\)')
        data = json.loads(p.search(resp).group(1))
        return data

    @staticmethod
    def __process_verify_code(pcid):
        url = 'http://login.sina.com.cn/cgi/pin.php?r={randint}&s=0&p={pcid}'.format(
            randint=int(random.random() * 1e8), pcid=pcid)
        filename = 'pin.png'
        if os.path.isfile(filename):
            os.remove(filename)

        urllib.urlretrieve(url, filename)
        if os.path.isfile(filename):  # get verify code successfully
            #  display the code and require to input
            # from PIL import Image
            # import subprocess
            # print filename
            # proc = subprocess.Popen(['display', filename])
            # code = raw_input('请输入验证码:')
            # os.remove(filename)
            # proc.kill()
            # 验证码自动识别
            code = img_code.get_img_result(filename)
            #print "code is ", code
            return dict(pcid=pcid, door=code)
        else:
            return dict()

    def login(self):
        info = self.__prelogin()

        login_data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': '',
            'pcid': '',
            'door': '',
            'vsnf': '1',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv': '',
            'sp': '',
            'sr': '',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        if 'showpin' in info and info['showpin']:  # need to input verify code
            login_data.update(self.__process_verify_code(info['pcid']))
        login_data['servertime'] = info['servertime']
        login_data['nonce'] = info['nonce']
        login_data['rsakv'] = info['rsakv']
        login_data['su'] = self.username
        login_data['sp'] = self.__encode_password(self.password, info)

        return self.__do_login(login_data)

    def __do_login(self, data):
        url = 'http://login.sina.com.cn/sso/login.php?client=%s' % __client_js_ver__
        headers = {
            'User-Agent': 'Weibo Assist'
        }
        req = urllib2.Request(
            url=url, data=urllib.urlencode(data), headers=headers)
        resp = urllib2.urlopen(req).read()

        return self.__parse_real_login_and_do(resp)

    def __parse_real_login_and_do(self, resp):
        p = re.compile('replace\(["\'](.+)["\']\)')
        url = p.search(resp).group(1)

        # parse url to check whether login successfully
        query = urlparse.parse_qs(urlparse.urlparse(url).query)
        if int(query['retcode'][0]) == 0:  # successful
            self.opener.open(url)  # log in and get cookies
            #print u'登录成功!'
            return True
        else:  # fail
            print u'错误代码:', query['retcode'][0]
            print u'错误提示:', query['reason'][0].decode('gbk')
            return False

    def urlopen(self, url):
        return self.opener.open(url)

    def get_cookie(self):
        return self.cj

    """
    功能：解析微博视频的html页面
    输入：html，输入页面文本
    返回：打印输出json字符串
    """
    def parse_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        ul = soup.find('ul', {"class": "li_list_1"})
        alist = ul.find_all('a')
        sqldata = {}
        for anode in alist:
            self.end_id = anode['mid'] #最后一个id，赋值为类成员变量
            href = anode['href']
            vid = href[6:15]
            play_url = "https://weibo.com" + href
            sqldata['vid'] = vid
            sqldata['title'] = anode.find('div', {"class": "txt_cut"}).get_text()
            sqldata['thumbnail'] = anode.find('img', {"class": "piccut"})['src']
            # 能下载的地址
            (short_url, duration,view_count) = self.get_video_url(play_url)
            sqldata['link'] = play_url
            sqldata['duration'] = duration
            sqldata['view_count'] = view_count
            if (sqldata['link'] == 404):
                continue
            anode.find('em', {"class": "L_ficon ficon_btn_on"}).decompose()
            #play_count = anode.find('div', {"class": "item_b L_fr"}).get_text()
            #play_count = ''.join(x for x in play_count if ord(x) < 256)
            #sqldata['view_count'] = play_count
            sqldata['source'] = "weibo"
            sqldata['category'] = "vfun"
            sqldata['username'] = anode.find('div', {"class": "item_a L_autocut L_fl"}).get_text()
            sqldata['appbk_category'] = '搞笑'
            sqldata['fetch_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print json.dumps(sqldata)

    """
    功能：获得微博视频2页面之后的url
    输入：num， 页码，>=2
    返回：微博视频第二页之后的url
    """
    def get_page_url(self, num):
        return "http://weibo.com/p/aj/v6/mblog/videolist?type=vfun&page=" + str(num) +\
               "&end_id=" + self.end_id + "&__rnd=" + self.time_str

    """
    功能：获得二级链接内容，为视频内容链接，重启播放的url，可下载视频文件
    输入：url， 视频内容链接
    输出：short_url， 视频短链接
    """
    def get_video_url(self,url):
        html = self.urlopen(url).read()

        if 'weibo404.css' in html:
            return 404
        soup = BeautifulSoup(html,"html.parser")

        url_pa = soup.find('div',{'node-type':'common_video_player'})['action-data']
        params = urlparse.parse_qs(url_pa) #解析url get参数，获得视频短url
        short_url = params["short_url"][0]
        #duration = params["duration"][0]
        duration = 100
        view_count = params["play_count"][0].replace("万", "0000")
        return (short_url, duration,view_count)

    """
    功能：解析微博视频的json格式页面
    输入：json_text，输入页面文本
    返回：打印输出json字符串
    """
    def parse_json(self, json_text):
        soup = BeautifulSoup(json_text, "html.parser")
        alist = soup.find_all('a')
        sqldata = {}
        for anode in alist:
            self.end_id = anode['mid'] #最后一个id，赋值为类成员变量
            href = anode['href']
            vid = href[6:15]
            play_url = "https://weibo.com"+href
            sqldata['vid'] = vid
            sqldata['title'] = anode.find('div', {"class": "txt_cut"}).get_text()
            sqldata['thumbnail'] =  anode.find('img', {"class": "piccut"})['src']
            #能下载的地址
            (short_url, duration,view_count) = self.get_video_url(play_url)
            sqldata['link'] = play_url
            sqldata['duration'] = duration
            sqldata['view_count'] = view_count
            if(sqldata['link'] ==404 ):
                continue
            #anode.find('em', {"class": "L_ficon ficon_btn_on"}).decompose()
            #play_count = anode.find('div', {"class": "item_b L_fr"}).get_text()
            #play_count = ''.join(x for x in play_count if ord(x) < 256)
            #sqldata['view_count'] = play_count
            sqldata['source'] = "weibo"
            sqldata['category'] = "vfun"
            sqldata['username'] = anode.find('div', {"class": "item_a L_autocut L_fl"}).get_text()
            sqldata['appbk_category'] = '搞笑'
            sqldata['fetch_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print json.dumps(sqldata)

    """
    功能：获得微博视频内容信息
    输入：num，翻页个数
    返回：打印输出全部数据
    """
    def get_video_list(self,num=6):
        #下载第1页
        base_url = "http://weibo.com/tv/vfun"
        html = self.urlopen(base_url).read()
        self.parse_html(html) #打印输出

        
        #下载第2-6页
        for num in range(2, num+1):
            page_url = self.get_page_url(num)
            content = self.urlopen(page_url).read()
            html = json.loads(content)["data"]["data"] #value是一个html字符串
            self.parse_json(html) #打印输出

if __name__=="__main__":
    #step 1,微博登录
    weibo = Weibo('h194@163.com', 'h194h194h194h194')
    # 登录后抓取
    if weibo.login():
        weibo.get_video_list()
