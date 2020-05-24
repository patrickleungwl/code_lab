#!/usr/bin/python

import sys

while True:
    strin = sys.stdin.readline()
    strin = strin.strip()
    num = int(strin)
    num = num*2
    print('%i %s' % (num, strin))

#strin = sys.stdin.readline()
#strin = strin.strip()
#num = int(strin)
#num = num*3
#print('%i %s' % (num, strin))
#
#print('end')
