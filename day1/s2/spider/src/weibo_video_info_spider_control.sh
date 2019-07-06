#!/bin/sh
#微博视频基础信息下载
#step 1, 下载视频信息数据
./weibo_video_spider.py  > weibo.json
#step 2, 入库
./insert_sql.py weibo.json video_info
