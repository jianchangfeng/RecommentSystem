#!/bin/sh
#检查check_thread.sh进程是否存在，若不存在，则调用脚本启动check_thread.sh
#set -x
source ./exe_file
exist=`ps -ef |awk '{print $9" "$10" "$11}'| grep "^./check_thread.sh $exe $serv_port$" | wc -l`
if [[ $exist -ge 1 ]]
then
    echo "check_thread.sh $exe  $serv_port has started!"
else
    nohup ./check_thread.sh $exe $serv_port >> check_thread.dat &
    echo "start check thread sh success!"
fi
