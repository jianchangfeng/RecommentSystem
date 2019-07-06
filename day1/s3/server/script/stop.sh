#!/bin/bash
#对进程进行关闭操作；进程存在的话，就找出其进程号，进行kill；并检查是否kill成功

set -x
source exe_file

max_check_time=10
check_time=0

# if the process is not working, do nothing
exist=`ps -ef |awk '{print $9" " $10 }'| grep "^./$exe $serv_port$" | wc -l`
if [[ $exist != 1 ]]; then
    echo "$exe  $serv_port not exist!"
    exit 1
fi

# stop the process
pid=`ps aux|grep "./$exe $serv_port$" |grep -v grep|awk '{print $2}'`
#echo "$pid"
kill $pid

# check the program
check_time=0
while [[ 1 ]]; do
    exist=`ps -ef |awk '{print $9" " $10 }'| grep "^./$exe $serv_port$" | wc -l`
    if [[ $exist != 1 ]]; then
        echo "$exe  $serv_port stop succ!"
        break;
    fi
    let check_time+=1
    if [ $check_time -gt $max_check_time ]; then
        echo "$exe  $serv_port stop failed!"
        break;
    fi
    sleep 1
done

