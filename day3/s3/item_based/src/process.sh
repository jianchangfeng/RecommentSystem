#!/bin/sh
#########################################################################
# Author: billczhang
# Created Time: Sun 16 Jul 2017 03:22:56 PM CST
# File Name: process.sh
# Description: 
#########################################################################
cat action.dat|awk '{print $1"\t"$2}'|sort -k1,1|./item_sim_reducer1.py|sort -k1,1|./item_sim_reducer2.py > item_based.dat

