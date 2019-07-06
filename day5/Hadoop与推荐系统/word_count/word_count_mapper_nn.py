#!/usr/bin/env python
#coding=utf-8
import sys
import os


def output(line):
    print(line + "\t"+"1")

for line in sys.stdin:
    line = line.strip()
    output(line)
