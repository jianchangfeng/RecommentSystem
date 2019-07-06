#!/bin/sh
set -x
source ./exe_file
pid=`ps aux|grep "check_thread.sh ${exe} ${serv_port}"|grep -v grep|awk '{print $2}'`
if [ ${#pid} -gt 1 ]
then
    echo "current check thread " ${pid}
    kill -9 ${pid}
    echo "check_thread.sh $exe $serv_port killed"
fi
