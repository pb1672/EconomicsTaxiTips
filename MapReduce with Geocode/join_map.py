#!/usr/bin/python

import sys
import os
import re

currentFile = None

for line in sys.stdin:
    if os.environ.get("mapreduce_map_input_file") != currentFile:
        currentFile = os.environ.get("mapreduce_map_input_file")
        continue
    else:
        l = line.strip().split(",")
        if re.search(r'fare', os.environ.get("mapreduce_map_input_file")):
            key = (l[0], l[1], l[2], l[3])
            value = ("Fares", l[4:])
        elif re.search(r'trip', os.environ.get("mapreduce_map_input_file")):
            key = (l[0], l[1], l[2], l[5])
            value = ("Trips", list(l[i] for i in range(len(l)) if i not in [0, 1, 2, 5]))
        print "%s\t%s" % (key, value)