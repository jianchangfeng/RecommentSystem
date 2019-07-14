#!/bin/sh
#set -x
#数据库连接信息
#新数据库,内网
db_host='rm-bp1w81w3y5da24ape.mysql.rds.aliyuncs.com'
db_user='rootali'
db_pw='Rootali1'
db_name='short_video'

item_file=$1

data_num=`wc -l $1`

echo "___________________________begin load search data file_________________________"
echo [`date "+%Y-%m-%d %H:%M:%S"`] "begin insert, data num: " ${data_num}


#load 入表
mysql -h${db_host} -u${db_user} -p${db_pw} -t ${db_name} -e "LOAD DATA local INFILE '"${item_file}"' into table user_action FIELDS TERMINATED BY '\t' (uid,source_vid,action)"


echo [`date "+%Y-%m-%d %H:%M:%S"`] 'finish update online table'

