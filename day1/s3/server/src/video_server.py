#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Thu 15 Jun 2017 02:46:08 PM CST
# File Name: video_server.py
# Description: 
######################################################################
import json
import time
import sys
import web
import video_rec

# reload(sys)
# sys.setdefaultencoding('utf8')

urls = ('/hello', 'hello',  # 测试服务
        '/get_videos_by_category', 'videos_by_category',  # 推荐列表
        '/get_videos_by_search', 'videos_by_search',  # 视频搜索
        '/add_action', 'action',  # 添加用户行为
        '/get_video', 'video',  # 获得一个视频的信息
        '/get_relate_videos', 'relate_videos',  # 获得一个视频的相关视频
        )


class hello:
    def GET(self):
        return "hello"


class videos_by_category:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')
        param = web.input(c="搞笑", start=0, limit=10, uid=0, pid=0)
        c = param.c  # 类别
        start = param.start  # 开始位置
        limit = param.limit  # 取多少记录
        uid = param.uid  # 用户id
        pid = param.uid  # 平台id
        result = video_rec.get_videos_by_category(c, start, limit, uid, pid)
        return result


# 获得视频搜索结果
class videos_by_search:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')
        param = web.input(n="搞笑", start=0, limit=10)
        n = param.n  # 搜索词
        start = param.start  # 开始位置
        limit = param.limit  # 取多少记录
        return 0


# 添加用户行为
class action:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')
        param = web.input(uid=0, id=0, action="OPEN", pid=0)
        uid = param.uid  # 用户id
        id = param.id  # 视频内部id
        action = param.action  # 用户行为
        pid = param.uid  # 平台id
        return 0


# 获得一个视频的信息
class video:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')
        param = web.input(id=0)
        id = param.id  # 视频内部id
        result = video_rec.get_video(id)
        return result


# 获得一个视频的相关视频
class relate_videos:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')
        param = web.input(uid=0, id=0)
        uid = param.uid  # 用户id
        id = param.id  # 视频内部id
        return 0


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
