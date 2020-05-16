import sys
import math
import itertools


# get_next_code
#
# given 
#   codes = a code array 
#   idx   = the current location
# return
#   array of instructions [1,a,b,c]
#   location of next idx
#
# 99 - stop
# 1,a,b,c - read from positions a and b and store the sum in c
# 2,a,b,c - read from positions a and b and store the product in c
# advance by 4 positions
# 3,a - take input and put into position a
# 4,a - take a and send to output
# 5,a,b - if a != 0, then set IP to b
# 6,a,b - if a == 0, then set IP to b
# 7,a,b,c - if a < b, then put 1 into c, else put 0 into c
# 8,a,b,c - if a == b, then put 1 into c, else put 0 into c

def get_next_code(codes,idx):
    code = codes[idx]
    results = []
    return_idx = idx

    opcode_modes = get_parameter_modes(code)
    opcode = opcode_modes[0]
    pm1 = opcode_modes[1]
    pm2 = opcode_modes[2]
    pm3 = opcode_modes[3]

    if opcode == 99:
        results.append(99)
        return_idx = -1
    if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
        results.append(opcode)
        if pm1 == 0:
            addr1 = codes[idx+1]
            results.append(codes[addr1])
        if pm1 == 1:
            value = codes[idx+1]
            results.append(value)
        if pm2 == 0:
            addr2 = codes[idx+2]
            results.append(codes[addr2])
        if pm2 == 1:
            value = codes[idx+2]
            results.append(value)
        results.append(codes[idx+3])
        return_idx = idx+4
    if opcode == 3:
        results.append(opcode)
        results.append(codes[idx+1])
        return_idx = idx+2
    if opcode == 4:
        results.append(opcode)
        if pm1 == 0:
            addr1 = codes[idx+1]
            results.append(codes[addr1])
        if pm1 == 1: 
            value = codes[idx+1]
            results.append(value)
        return_idx = idx+2
    if opcode == 5 or opcode == 6:
        results.append(opcode)
        if pm1 == 0:
            addr1 = codes[idx+1]
            results.append(codes[addr1])
        if pm1 == 1: 
            value = codes[idx+1]
            results.append(value)
        if pm2 == 0:
            addr2 = codes[idx+2]
            results.append(codes[addr2])
        if pm2 == 1: 
            value = codes[idx+2]
            results.append(value)
        return_idx = idx+3

    return (results,return_idx)


# split_string
# given:    comma delimited string
# returns:  array of integers

def split_string(input):
    codes = input.split(',')
    for i in range(0,len(codes)):
        codes[i] = int(codes[i])
    return codes 

# combine_codes
# given:    an array of integers
# returns:  a comma delmited string of integers

def combine_codes(codes):
    for i in range(0,len(codes)):
        codes[i] = str(codes[i])
    return ','.join(codes)

# get_parameter_modes
# given:   integer code
# return:  array of opcode, pm1, pm2, pm3
# example: 
#  ABCDE
#   1002
#
# two digit opcode= 02
# C = 1st parameter mode = 0, position mode
# D = 2nd parameter mode = 1, immediate mode
# E = 3rd parameter mode = 2, position mode
#  assert(get_parameter_modes(11002)==[0,1,1])

def get_parameter_modes(code):
    code_str = '%05i' % (code)
    opcode = int(code_str[3:])
    pm1 = int(code_str[2])
    pm2 = int(code_str[1])
    pm3 = int(code_str[0])
    return [opcode,pm1,pm2,pm3]

# input is intcode program

def run_amp(input_str):

    cout_results = ''
    codes = split_string(input_str)
    input_num = 0
    next_idx = 0
    while True:
        (results,next_idx) = get_next_code(codes,next_idx)
        opcode = results[0]
        if opcode == 99:
            break
        if opcode == 5:
            param1 = results[1]
            param2 = results[2]
            if param1 != 0:
                next_idx = param2

        if opcode == 6:
            param1 = results[1]
            param2 = results[2]
            if param1 == 0:
                next_idx = param2

        if opcode == 1 or opcode == 2:
            param1 = results[1]
            param2 = results[2]
            trgt  = results[3]

            if opcode == 1:
                codes[trgt] = param1 + param2
            if opcode == 2:
                codes[trgt] = param1 * param2

        if opcode == 3:
            trgt = results[1]
            # read from stdin
            strin = sys.stdin.readline()
            codes[trgt] = int(strin.strip())

        if opcode == 4:
            trgt = results[1]
            print('%i\n' % (trgt))

        if opcode == 7:
            param1 = results[1]
            param2 = results[2]
            trgt  = results[3]
            codes[trgt] = 0
            if param1 < param2:
                codes[trgt] = 1

        if opcode == 8:
            param1 = results[1]
            param2 = results[2]
            trgt  = results[3]
            codes[trgt] = 0
            if param1 == param2:
                codes[trgt] = 1

    return (combine_codes(codes),cout_results.strip())





