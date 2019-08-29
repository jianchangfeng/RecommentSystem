#!/usr/bin/env python
#coding=utf-8
import sys
import os


def output(line):
    item_list = line.split()
    print (item_list[0] + "\t" + item_list[1])

for line in sys.stdin:
    line = line.strip()
    output(line)
