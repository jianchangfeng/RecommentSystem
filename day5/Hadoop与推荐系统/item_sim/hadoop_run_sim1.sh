#!/bin/bash
#########################################################################
# Author: billczhang
# Created Time: Fri 31 May 2019 07:44:52 PM CST
# File Name: hadoop_run_sim1_test.sh
# Description: 
#########################################################################

hadoop fs -rm -r /video/maris/item_sim/output
#hadoop org.apache.hadoop.streaming.HadoopStreaming \
hadoop jar /bigdata/hadoop-2.8.5/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar \
    -D mapreduce.job.reduces=1 \
    -input /video/maris/item_sim/input/* \
    -output /video/maris/item_sim/output \
    -mapper "python item_sim_mapper1.py" \
    -reducer "python item_sim_reducer1.py" \
    -file item_sim_mapper1.py \
    -file item_sim_reducer1.py \

#get data
