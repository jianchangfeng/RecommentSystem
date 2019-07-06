#!/usr/bin/env python
#coding=utf-8
import sys
import urllib2
import urllib
import re
import json
import time
from mns.account import Account
from mns.queue import *
from mns.topic import *
from mns.subscription import *
import ConfigParser

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
    # 从https://account.console.aliyun.com/#/secure获取$YourAccountid
    # 从https://ak-console.aliyun.com/#/accesskey获取$YourAccessId和$YourAccessKey
    # 从http://$YourAccountId.mns.cn-hangzhou.aliyuncs.com获取$YourMNSEndpoint, eg. http://1234567890123456.mns.cn-hangzhou.aliyuncs.com
    YourMNSEndpoint = "http://1111641897067585.mns.cn-hangzhou-internal.aliyuncs.com/"
    YourAccessId = "LTAIyhZeIPt8ivJd"
    YourAccessKey = "myvAcplJMk32PHIt2DSmWhRqcz6CHv"
    my_account = Account(YourMNSEndpoint, YourAccessId, YourAccessKey)

    YourTopicName = "sms.topic-cn-hangzhou"
    my_topic = my_account.get_topic(YourTopicName)
    #print my_topic
    '''
    Step 2. 设置SMS消息体（必须）
    注：目前暂时不支持消息内容为空，需要指定消息内容，不为空即可。
    '''
    msg_body1 = "报警短信消息"
    '''
    Step 3. 生成SMS消息属性，single=False表示每个接收者参数不一样，
    single=True表示每个接收者参数一样
    '''
    # 3.1 设置SMSSignName和SMSTempateCode
    YourSignName = "app运营助手"
    YourSMSTemplateCode = "SMS_32785106"

    direct_sms_attr1 = DirectSMSInfo(free_sign_name=YourSignName, template_code=YourSMSTemplateCode, single=True)
    # 3.2 指定接收短信的手机号并指定发送给该接收人的短信中的参数值（在短信模板中定义的）
    cur_time = time.strftime('%H:%M:%S', time.localtime()) #变量内容不能太长
    direct_sms_attr1.add_receiver(receiver=tel)
    direct_sms_attr1.set_params({"machine":"短视频","module":module,"time":cur_time,"message":message})

    #Step 5. 生成SMS消息对象
    msg1 = TopicMessage(msg_body1, direct_sms=direct_sms_attr1)

    re_msg = my_topic.publish_message(msg1)
    #print "Publish Message Succeed. MessageBody:%s MessageID:%s" % (msg_body1, re_msg.message_id)

    return 0

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "please input tel,module,message"
        print "example:./send_message.py 18611846371 word_rank error"
        sys.exit()

    tel = sys.argv[1]
    module = sys.argv[2]
    message = sys.argv[3]
    print send_message(tel, module, message)