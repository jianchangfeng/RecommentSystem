#!/bin/sh
#set -x
#数据库连接信息
#新数据库,内网
#db_host='rm-bp1w81w3y5da24ape.mysql.rds.aliyuncs.com'
#db_user='rootali'
#db_pw='Rootali1'
#db_name='short_video'
db_host="rm-2zemcvpd7o8r668n7do.mysql.rds.aliyuncs.com"  # 线上机器
db_user="root"
db_pw="Jcfcxl_1314"
db_name="short_video"  # 数据库名
item_file=$1

data_num=`wc -l $1`

echo "___________________________begin load search data file_________________________"
echo [`date "+%Y-%m-%d %H:%M:%S"`] "begin insert, data num: " ${data_num}


#load 入表
mysql -h${db_host} -u${db_user} -p${db_pw} -t ${db_name} -e "LOAD DATA local INFILE '"${item_file}"' REPLACE into table item_based_rec FIELDS TERMINATED BY '\t' (vid1,vid2,sim)"


echo [`date "+%Y-%m-%d %H:%M:%S"`] 'finish update online table'


