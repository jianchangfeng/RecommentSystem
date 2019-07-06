#!/bin/sh
cat action.dat|./item_sim_mapper1.py|sort -k1,1|./item_sim_reducer1.py|sort -k1,1|./item_sim_reducer2.py > item_based.dat
#cat action.dat|awk '{print $1"\t"$2}'|sort -k1,1|./item_sim_reducer1.py|sort -k1,1|./item_sim_reducer2.py > item_based.dat
