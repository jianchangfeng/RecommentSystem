#!/bin/sh
set -x
#hadoop 基准测试，测试hadoop是否出问题
hadoop fs -rm -r /video/maris/word_count/output
#hadoop org.apache.hadoop.streaming.HadoopStreaming \
hadoop jar /bigdata/hadoop-2.8.5/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar \
    -D mapreduce.job.reduces=1 \
    -input /video/maris/word_count/input/ \
    -output /video/maris/word_count/output \
    -mapper "python word_count_mapper.py" \
    -reducer "python word_count_reducer.py" \
    -file word_count_mapper.py \
    -file word_count_reducer.py
#get data
#hadoop fs -get /video/maris/word_count/output/part-0* ./
