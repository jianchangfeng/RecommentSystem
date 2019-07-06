#!/bin/sh
source exe_file
if [ $# -ne 1 ]
then
    echo "please input message body"
    exit
fi
send_rtx_exe="sendrtxproxy"
send_message=$1
sender="mariswang"
receiver="mariswang;talisaliu"
module=${exe}

#${send_rtx_exe} "${sender}" "${receiver}" "${module}" "${send_message}" 1
