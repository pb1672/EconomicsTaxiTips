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
            fare = float(l[5])
            surcharge = float(l[6])
            tip = float(l[8])
            tolls = float(l[9])
            revenue = fare + surcharge + tip + tolls
            if revenue > 0:
                tipPerCent = tip / revenue * 100
            else:
                tipPerCent = 0
            value = ("Fares", tipPerCent)
        elif re.search(r'trip', os.environ.get("mapreduce_map_input_file")):
            key = (l[0], l[1], l[2], l[5])
            value = ("Trips", list(l[i] for i in range(7,14)))
        print "%s\t%s" % (key, value)