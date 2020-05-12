import sys
import math

def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


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
    if opcode == 1 or opcode == 2:
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

def run_program(input_str,input_value=-1):
    codes = split_string(input_str)
    next_idx = 0
    while True:
        (results,next_idx) = get_next_code(codes,next_idx)
        opcode = results[0]
        if opcode == 99:
            break
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
            codes[trgt] = input_value
        if opcode == 4:
            trgt = results[1]
            print('%i' % (trgt))            
    return combine_codes(codes)


assert(get_next_code([104,10,20,30,40],0)==([4,10],2))
assert(get_next_code([99,10,20,30,40],0)==([99],-1))
assert(get_next_code([11101,10,20,30,40],0)==([1,10,20,30],4))
assert(get_next_code([0,11101,10,20,30,40],1)==([1,10,20,30],5))
assert(get_next_code([0,1,11102,10,20,30,40],2)==([2,10,20,30],6))
assert(get_next_code([3,10,20,30,40],0)==([3,10],2))

test = '1,9,10,3,2,3,11,0,99,30,40,50'
assert(run_program(test)=='3500,9,10,70,2,3,11,0,99,30,40,50')
assert(run_program('1,0,0,0,99')=='2,0,0,0,99')
assert(run_program('2,3,0,3,99')=='2,3,0,6,99')
assert(run_program('2,4,4,5,99,0')=='2,4,4,5,99,9801')
assert(run_program('1,1,1,4,99,5,6,0,99')=='30,1,1,4,2,5,6,0,99')
assert(run_program('3,0,99',88)=='88,0,99')
assert(run_program('4,2,99')=='4,2,99')
assert(run_program('1101,100,-1,4,0')=='1101,100,-1,4,99')

assert(get_parameter_modes(2)==[2,0,0,0])
assert(get_parameter_modes(1002)==[2,0,1,0])
assert(get_parameter_modes(11002)==[2,0,1,1])

input = get_input(sys.argv[1])
print(input)
run_program(input,1)


