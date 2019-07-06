#!/bin/bash
#判断程序是否已经启动，未启动的话，①进行启动；②检查启动是否正常；③监听一下启动进程的端口是否正常运行

#set -x
source ./exe_file

max_check_time=10
check_time=0

# if the process is already working, do nothing
exist=`ps -ef |awk '{print $9" " $10 }'| grep "^./$exe $serv_port$" | wc -l`
if [[ $exist == 1 ]]; then
    echo "$exe $serv_port already exist!"
    exit 1
else
    echo "$exe $serv_port not exist!"
fi

cd ../src/

# start the program
ulimit -c unlimited
export LD_LIBRARY_PATH=/usr/local/lib
nohup ./${exe}  ${serv_port}> nohup.dat &

# check the program
check_time=0
while [[ 1 ]]
do
    exist=`ps -ef |awk '{print $9" " $10 }'| grep "^./$exe $serv_port$" | wc -l`
    if [[ $exist == 1 ]]; then
        echo "$exe $serv_port start OK"
        break
    fi
    let check_time+=1
    if [ $check_time -gt $max_check_time ]; then
        echo "$exe $serv_port start failed!"
        break;
    fi
    sleep 1
done

# check listen port
while [[ 1 ]]
do
    exist=`netstat -nal | grep LISTEN | grep $serv_port | grep -v grep | wc -l`
    if [[ $exist == 1 ]]; then
        echo "ServPort $serv_port listen OK"
        break
    fi
    let check_time+=1
    if [ $check_time -gt $max_check_time ]; then
        echo "ServPort $ser_port is not listening!"
        break;
    fi
    sleep 1
done
cd -
