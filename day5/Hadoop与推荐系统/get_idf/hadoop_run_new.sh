#!/bin/sh
#hadoop idf,需首先自行创建相关目录，并把数据put到input目录
# 压缩文件包
cd src 
rm get_idf.tar.gz
tar -czvf get_idf.tar.gz *
hadoop fs -rm /video/maris/get_idf/get_idf.tar.gz
hadoop fs -put get_idf.tar.gz /video/maris/get_idf/
cd -

#开始执行hadoop操作
hadoop fs -rm -r /video/maris/get_idf/output
#hadoop org.apache.hadoop.streaming.HadoopStreaming \
hadoop jar /bigdata/hadoop-2.8.5/share/hadoop/tools/lib/hadoop-streaming-2.8.5.jar \
    -archives  hdfs:///video/maris/get_idf/get_idf.tar.gz#get_idf \
    -D mapreduce.job.reduces=1 \
    -D mapreduce.job.task=2 \
    -input /video/maris/get_idf/input/* \
    -output /video/maris/get_idf/output \
    -mapper "python get_idf/get_idf_mapper.py" \
    -reducer "python get_idf/get_idf_reducer.py" \
   
    
  
#get data
#hadoop fs -get /video/maris/get_idf/output/part-0* ./
