#!/bin/sh
set -x
#视频数据下载
#step1 下载视频数据
./get_video_link.py > video_info.dat
#step2 存入到data目录下
./download_video.sh video_info.dat
 
