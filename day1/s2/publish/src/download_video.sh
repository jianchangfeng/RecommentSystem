#!/bin/sh
#通过you-get下载视频文件,存储在 ./videofile下
set -x
if [ $# -ne 1 ]
then
    echo "please input video link data file name"
    exit
fi

filename=$1
data_path="../data" #文件存储路径
cat $filename|while read line
do
    echo date ": process " $line
    link=`echo $line|awk '{print $1}'` #视频链接
    video_name=`echo $line|awk '{print $2}'` #视频文件名称,不包括扩展名
    echo $link , $video_name
    #下载视频,统一为mp4格式,下载文件会带上扩展名.mp4,但部分不带。。。
    #you-get --output-filename=${data_path}/${video_name} --format=mp4 --debug $link
    you-get --output-filename=${data_path}/${video_name} $link
    if [ $? -ne 0 ] #下载出错则报警
    then
        echo "you-get link $link error"
        #./send_message.py 18611846371 'you-get error!' #发送报警短信
    else
            if [ -f "${data_path}/${video_name}" ] #如果下载成功,但没有加mp4扩展名，给加上
            then
                mv ${data_path}/${video_name} ${data_path}/${video_name}.mp4
            fi
            if [ -f "${data_path}/${video_name}.mp4" ] #如果下载成功,打一个标记
            then
                touch ${data_path}/${video_name}.sign 
            fi
    fi
done
