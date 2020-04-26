import sys
import math
import numpy as np
import datetime 

def get_input(file_input):
    tmp = ''
    with open(file_input) as f:
        tmp = f.readline()
    return tmp.strip()


def scan_input(input):

    diff = ord('a')-ord('A')
    print(len(input))
    for i in range(0,len(input)-1):
        left = input[i] 
        right = input[i+1]
        if abs(ord(left)-ord(right)) == diff:
            #print(left, right)
            after_zap = input[0:i] + input[i+2:]
            #print(after_zap)
            return after_zap
    return input

input = get_input(sys.argv[1])
while (True):
    result = scan_input(input)
    if result == input:
        break
    input = result

print(result)
print(len(result))
