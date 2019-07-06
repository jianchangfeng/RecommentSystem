#!/usr/bin/env python
#coding=utf-8
import sys 
import urllib2
import urllib
import re
import json
import time
reload(sys)
sys.setdefaultencoding('utf8')
#短信发送api


"""
fun:发送短信
input:tel , 向这个电话号码发送信息
input:module, 出错模块或者步骤名等
input:message, 出错信息
return 无
"""
def send_message(tel="18611846371",module="hadoop",message="error"):
    url = "https://api.leancloud.cn/1.1/requestSmsCode"
    request = urllib2.Request(url)
    request.add_header('X-LC-Id','wdVkR3HBdEm5JuxvUwx7a5ye')
    request.add_header('X-LC-Key','9F3g8WJXJaPlmGJXxBVU8BgV')
    request.add_header('Content-Type','application/json')
    data = {'mobilePhoneNumber':tel,
            'template':'appbk',
            'machine':'python_server',
            'module':module,
            'time':time.strftime('%m-%d %H:%M', time.localtime()),
            'message':message
            }
    
    response = urllib2.urlopen(request,json.dumps(data))
    text = response.read()
    return text

if __name__=="__main__":
    if len(sys.argv) != 4:
        print "please input tel,module,message"
        print "example:./send_message.py 18611846371 word_rank error"
        sys.exit()

    
    tel = sys.argv[1]
    module = sys.argv[2] #不能太长,注意print内容
    message = sys.argv[3] #不能太长,注意pirnt内容
    print send_message(tel, module, message)

