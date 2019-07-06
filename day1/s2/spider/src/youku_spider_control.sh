#!/bin/sh
#step 1,下载视频信息
cat category.dat |./youku_category_spider.py > youku.json

#step 2, 插入数据库
./insert_sql.py youku.json video_info
