#/bin/sh
#更新一个机器
source "./conf.txt"
if [ $# -ne 1 ]
then
    echo "please input machine id, like 0"
    exit
fi

#machine id
id=$1

#ip....
ip=${ip[$id]}
ssh_port=22
user="root"
passwd="Rootali1"
install_dir="/root"

#shell 命令
cmd="ls"
./run_remote.sh $ip $ssh_port $user $passwd "cd ${install_dir};$cmd" 
