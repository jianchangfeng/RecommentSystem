#!/bin/sh
set -x
cat word.dat|./word_count_mapper.py|sort -k1,1|./word_count_reducer.py
