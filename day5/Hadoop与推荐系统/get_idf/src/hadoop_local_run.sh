#!/bin/sh
#!/bin/sh
if [ $# -ne 1 ]
then
    echo "please input file name"
    exit
fi

filename=$1
cat ${filename}|./get_idf_mapper.py|sort -k1,1|./get_idf_reducer.py > df.dict

line_num=`wc -l $1|awk '{print $1}'`
awk -F "\t" '{print $1"\t"log('''$line_num'''/$2)/log(2)}' df.dict > idf.dict