#!/usr/bin/python

import sys

while True:
    # read an input
    strin = sys.stdin.readline()
    strin = strin.strip() 
    if strin == 'exit':
        break
    # send output
    sys.stdout.write('hello %s' % strin)

