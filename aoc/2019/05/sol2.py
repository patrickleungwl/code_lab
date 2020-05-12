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

def run_program(input_str,input_value=-1):
    cout_results = ''
    codes = split_string(input_str)
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
            codes[trgt] = input_value

        if opcode == 4:
            trgt = results[1]
            res = '%i\n' % (trgt)
            cout_results = cout_results + res

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


assert(get_next_code([104,10,20,30,40],0)==([4,10],2))
assert(get_next_code([99,10,20,30,40],0)==([99],-1))
assert(get_next_code([11101,10,20,30,40],0)==([1,10,20,30],4))
assert(get_next_code([0,11101,10,20,30,40],1)==([1,10,20,30],5))
assert(get_next_code([0,1,11102,10,20,30,40],2)==([2,10,20,30],6))
assert(get_next_code([3,10,20,30,40],0)==([3,10],2))
assert(get_next_code([1105,0,1],0)==([5,0,1],3))
assert(get_next_code([1106,0,1],0)==([6,0,1],3))

test = '1,9,10,3,2,3,11,0,99,30,40,50'
assert(run_program(test)[0]=='3500,9,10,70,2,3,11,0,99,30,40,50')
assert(run_program('1,0,0,0,99')[0]=='2,0,0,0,99')
assert(run_program('2,3,0,3,99')[0]=='2,3,0,6,99')
assert(run_program('2,4,4,5,99,0')[0]=='2,4,4,5,99,9801')
assert(run_program('1,1,1,4,99,5,6,0,99')[0]=='30,1,1,4,2,5,6,0,99')
assert(run_program('3,0,99',88)[0]=='88,0,99')
assert(run_program('4,2,99')[0]=='4,2,99')
assert(run_program('1101,100,-1,4,0')[0]=='1101,100,-1,4,99')

assert(get_parameter_modes(2)==[2,0,0,0])
assert(get_parameter_modes(1002)==[2,0,1,0])
assert(get_parameter_modes(11002)==[2,0,1,1])

# using position mode, if input is equal to 8, output 1 else 0
assert(run_program('3,9,8,9,10,9,4,9,99,-1,8',1)[1] == '0')
# using position mode, if input is equal to 8, output 1 else 0
assert(run_program('3,9,8,9,10,9,4,9,99,-1,8',8)[1] == '1')

# using position mode, if input is less than 8, output 1 else 0
assert(run_program('3,9,7,9,10,9,4,9,99,-1,8',7)[1] == '1')
# using position mode, if input is less than 8, output 1 else 0
assert(run_program('3,9,7,9,10,9,4,9,99,-1,8',8)[1] == '0')

# using immediate mode, if input is equal to 8, output 1 else 0
assert(run_program('3,3,1108,-1,8,3,4,3,99',1)[1] == '0')
# using immediate mode, if input is equal to 8, output 1 else 0
assert(run_program('3,3,1108,-1,8,3,4,3,99',8)[1] == '1')

# using immediate mode, if input is less than 8, output 1 else 0
assert(run_program('3,3,1107,-1,8,3,4,3,99',1)[1] == '1')
# using immediate mode, if input is less than 8, output 1 else 0
assert(run_program('3,3,1107,-1,8,3,4,3,99',8)[1] == '0')

# if input is 0, then output 0; else output 1
assert(run_program('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',0)[1] == '0')
# if input is 0, then output 0; else output 1
assert(run_program('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',1)[1] == '1')
# if input is 0, then output 0; else output 1
assert(run_program('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',8)[1] == '1')
# if input is 0, then output 0; else output 1
assert(run_program('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',-1)[1] == '1')

# if input is 0, then output 0; else output 1
assert(run_program('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',0)[1] == '0')
# if input is 0, then output 0; else output 1
assert(run_program('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',1)[1] == '1')
# if input is 0, then output 0; else output 1
assert(run_program('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',8)[1] == '1')
# if input is 0, then output 0; else output 1
assert(run_program('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',-1)[1] == '1')

# if input is less than 8, output 999
# if input is 8, output 1000
# if input is greater than 8, output 1001
large_test = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
large_test = large_test + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,'
large_test = large_test + '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'

assert(run_program(large_test,7)[1] == '999')
assert(run_program(large_test,8)[1] == '1000')
assert(run_program(large_test,9)[1] == '1001')

# run puzzle for real
input = get_input(sys.argv[1])
print(input)
(codes,cout_result) = run_program(input,5)
print(codes)
print(cout_result)


