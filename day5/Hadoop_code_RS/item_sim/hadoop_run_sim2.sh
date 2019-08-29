#!/bin/sh
set -x
hadoop fs -rm -r /video/maris/item_sim/output2
#hadoop org.apache.hadoop.streaming.HadoopStreaming \
#如果acton.dat过大,使用cacheFile
# -cacheFile hdfs:///video/maris/item_sim/input/action.dat#action.dat \
hadoop jar /bigdata/hadoop-2.8.5/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar \
    -D mapreduce.job.reduces=1 \
    -input /video/maris/item_sim/output/part* \
    -output /video/maris/item_sim/output2 \
    -mapper "item_sim_mapper2.py" \
    -reducer "item_sim_reducer2.py" \
    -file item_sim_mapper2.py \
    -file item_sim_reducer2.py \
    -file action.dat \

#get data
#hadoop fs -get /video/maris/item_sim/output2/part* ./
