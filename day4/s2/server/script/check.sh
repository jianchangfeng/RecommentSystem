#!/bin/bash
#监听进程是否已经正常启动，监听端口情况

#set -x
source exe_file
exist=`ps -ef |awk '{print $9" "$10}'| grep "^./$exe $serv_port$" | wc -l`
if [[ $exist == 1 ]]; then
    echo "$exe  $serv_port is OK!"
else
    echo "$exe  $serv_port not exist!"
fi

exist=`netstat -nal | grep LISTEN | grep $serv_port | grep -v grep | wc -l`
if [[ $exist == 1 ]]; then
    echo "ServPort $serv_port listen OK!"
else
    echo "ServPort $serv_port is not listening!"
fi

