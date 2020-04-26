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

    for i in range(0,len(input)-1):
        left = input[i] 
        right = input[i+1]
        if abs(ord(left)-ord(right)) == bro_diff:
            #print(left, right)
            after_zap = input[0:i] + input[i+2:]
            #print(after_zap)
            return after_zap
    return input


def remove_alpha(input, dead_char):
    # expect to get A,B,C
    #print('removing %s from %s' % (dead_char, input))
    first_char_to_remove = chr(dead_char)
    second_char_to_remove = chr(dead_char+bro_diff)
    input = input.replace(first_char_to_remove, '')
    input = input.replace(second_char_to_remove, '')
    #print('after remvoving ' + input) 
    return input


def test_string(input, dead_char):
    result = ''
    compacted = remove_alpha(input, dead_char)
    while (True):
        result = scan_input(compacted)
        if result == compacted:
            break
        compacted = result
    return len(result)


# iterate removing Aa...Bb...Cc....
bro_diff = ord('a')-ord('A')
input = get_input(sys.argv[1])

for dead_char in range(ord('D'),ord('Z')+1):
    compacted_size = test_string(input, dead_char)
    print('%s => %s' % (chr(dead_char), compacted_size))


