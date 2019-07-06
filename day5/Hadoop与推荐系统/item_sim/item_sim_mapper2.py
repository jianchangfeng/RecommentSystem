#!/usr/bin/env python
#coding=utf-8
import sys
import os


def output(line):
    print(line)

for line in sys.stdin:
    line = line.strip()
    output(line)
