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
#hadoop jar /opt/apps/ecm/service/hadoop/2.7.2/package/hadoop-2.7.2/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
hadoop jar /bigdata/hadoop-2.8.4/share/hadoop/tools/lib/hadoop-streaming-2.8.4.jar \
    -input /video/maris/get_idf/input/* \
    -output /video/maris/get_idf/output \
    -mapper "./get_idf/get_idf_mapper.py" \
    -reducer "./get_idf/get_idf_reducer.py" \
    -cacheArchive 'hdfs:///video/maris/get_idf/get_idf.tar.gz#get_idf' \
    -jobconf  mapred.reduce.tasks=2 \
    -jobconf  mapred.job.name="maris_get_idf"
#get data
hadoop fs -get /video/maris/get_idf/output/part-0* ./
