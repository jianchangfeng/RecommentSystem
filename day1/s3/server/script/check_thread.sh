#!/bin/sh

#一直循环，检查我们的程序是否正在执行：检查的为“程序名.py 端口号”
#程序在执行，则睡眠几秒，之后再查；若程序没有执行，则调用脚本重启执行
set -x
source ./exe_file

while true
do
    i=`ps -ef |awk '{print $9" " $10 }'| grep "^./$exe $serv_port$" | wc -l`

    if [ $i == 1 ]
    then
        sleep 10
    else
        echo "server down!" >> ../log/restart.log
        ./start.sh >> restart.log
        #send rtx messange
        ./send_message.py 13041166753 $exe $serv_port server_down
        echo "send message!"

        echo "`date` $exe $serv_port restart" >> ../log/restart.log
        sleep 30
    fi
done
