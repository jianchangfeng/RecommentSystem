#!/bin/sh
#发布视频文件到oss
#完成标记文件为*.sign, 视频文件为*.mp4
#视频文件发布完成后,更新数据库
data_path="../data/"
set -x
ls ${data_path}/*.sign|while read line
do
    #获得真实文件名,下面这个带路径
    video_file=`echo $line|sed 's/sign/mp4/'`
    #解析不带路径的
    filename=`echo ${video_file}|awk -F "/" '{print $NF}'`
    ossutil64 cp $video_file oss://appbkplay/play1/

    #判断上条命令是否执行成功；如果不成功，报警
    if [ $? -ne 0 ]
    then
        echo "put $video_file error"
        #send_message.py 18610754175 'osscmd' 'put file ERROR!'
    else #执行成功,删除,并更新数据库
        rm $line #删除标记文件
        rm $video_file #删除视频文件
        ./update_video_info.py $filename #更新数据库信息
    fi
done
