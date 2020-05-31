import sys
import math
import itertools

def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


def get_all_phases_combinations():
    allphases = []

    pm = itertools.permutations('01234')
    for p in pm:
        phases = []
        for i in range(0,len(p)):
            num = int(p[i])
            phases.append(num)
        allphases.append(phases)
    return allphases


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

def get_next_code(codes,idx,relative_base=-1):
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

        # pm1 = mode of parameter 1
        # mode 0 is position mode- addr1 of 50 means address at cell 50
        # mode 1 is immediate mode- value of 50 
        # mode 2 is relative mode- addr1 of 50 means 50 + relative base
        if pm1 == 0:
            addr1 = codes[idx+1]
            results.append(codes[addr1])
        if pm1 == 1:
            value = codes[idx+1]
            results.append(value)
        if pm1 == 2:
            addr1 = codes[idx+1] + relative_base
            results.append(codes[addr1])

        # pm2 = mode of parameter 2
        if pm2 == 0:
            addr2 = codes[idx+2]
            results.append(codes[addr2])
        if pm2 == 1:
            value = codes[idx+2]
            results.append(value)
        if pm2 == 2:
            addr2 = codes[idx+2] + relative_base
            results.append(codes[addr2])

        # pm3 
        if pm3 == 0:
            addr3 = idx+3
            results.append(codes[addr3])
        if pm3 == 1:
            value = codes[idx+3]
            results.append(value)
        if pm3 == 2:
            addr3 = idx+3 + relative_base
            results.append(codes[addr3])

        return_idx = idx+4

    if opcode == 3:
        results.append(opcode)
        if pm1 == 0: 
            addr1 = codes[idx+1]
            results.append(addr1)
        if pm1 == 2:
            addr1 = codes[idx+1] + relative_base
            results.append(addr1)
        return_idx = idx+2

    if opcode == 4:
        results.append(opcode)
        if pm1 == 0:
            addr1 = codes[idx+1]
            results.append(codes[addr1])
        if pm1 == 1: 
            value = codes[idx+1]
            results.append(value)
        if pm1 == 2:
            addr1 = codes[idx+1] + relative_base
            results.append(codes[addr1])
        return_idx = idx+2


    if opcode == 5 or opcode == 6:
        results.append(opcode)
        if pm1 == 0:
            addr1 = codes[idx+1]
            results.append(codes[addr1])
        if pm1 == 1: 
            value = codes[idx+1]
            results.append(value)
        if pm2 == 2:
            addr1 = codes[idx+1] + relative_base
            results.append(codes[addr1])

        if pm2 == 0:
            addr2 = codes[idx+2]
            results.append(codes[addr2])
        if pm2 == 1: 
            value = codes[idx+2]
            results.append(value)
        if pm2 == 2:
            addr2 = codes[idx+2] + relative_base
            results.append(codes[addr2])
        return_idx = idx+3


    if opcode == 9:
        results.append(opcode)
        if pm1 == 0:
            addr1 = codes[idx+1]
            new_base = relative_base + codes[addr1]
            relative_base = new_base
        if pm1 == 1:
            value = codes[idx+1]
            new_base = relative_base + value
            relative_base = new_base
        if pm1 == 2:
            addr1 = codes[idx+1] + relative_base
            new_base = relative_base + codes[addr1]
            relative_base = new_base
        return_idx = idx+2

    return (results,return_idx,relative_base)


# split_string
# given:    comma delimited string
# returns:  array of integers

def split_string(input,uprange):
    codes = input.split(',')

    # initialise memory up to 1m
    for i in range(0,uprange):
        codes.append(0)

    for i in range(0,len(codes)):
        codes[i] = int(codes[i])
    return codes 

# combine_codes
# given:    an array of integers
# returns:  a comma delmited string of integers

def combine_codes(codes):
    # find max cell with value
    max = len(codes)-1
    while max > 0:
        if codes[max] > 0:
            break
        max = max-1
    realcodes = []
    for i in range(0,max+1):
        realcodes.append(str(codes[i]))
    return ','.join(realcodes)



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

def run_program(input_str,input_value=-99,input_phase=-99):

    debug = 0
    if input_value == 888:
        debug = 1

    relative_base = 0
    cout_results = ''

    uprange = 1000
    if input_value == 1: 
        uprange = 1000000
    codes = split_string(input_str,uprange)
    input_num = 0
    next_idx = 0
    while True:
        (results,next_idx,relative_base) = get_next_code(codes,next_idx,relative_base)
        opcode = results[0]
        if opcode == 9:  # just update the relatve_base
            continue
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
            if input_phase < -98 and input_value < -98:
                print('problem')
                return -1
            if input_phase >= 0:
                codes[trgt] = input_phase
                input_phase = -1
            else:
                codes[trgt] = input_value
                input_value = -1

        if opcode == 4:
            trgt = results[1]
            res = '%i,' % (trgt)
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

        if debug == 1:
            print(codes[:10])

    results = cout_results.strip()
    results = results[:len(results)-1]
    return (combine_codes(codes),results)


assert(get_next_code([104,10,20,30,40],0)==([4,10],2,-1))
assert(get_next_code([99,10,20,30,40],0)==([99],-1,-1))
assert(get_next_code([11101,10,20,30,40],0)==([1,10,20,30],4,-1))
assert(get_next_code([0,11101,10,20,30,40],1)==([1,10,20,30],5,-1))
assert(get_next_code([0,1,11102,10,20,30,40],2)==([2,10,20,30],6,-1))
assert(get_next_code([3,10,20,30,40],0)==([3,10],2,-1))
assert(get_next_code([1105,0,1],0)==([5,0,1],3,-1))
assert(get_next_code([1106,0,1],0)==([6,0,1],3,-1))

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
assert(get_parameter_modes(109)==[9,1,0,0])

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

program = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
assert(run_program(program)[1] == program)

program = '1102,34915192,34915192,7,4,7,99,0'
assert(run_program(program)[1] == '1219070632396864')

program = '104,1125899906842624,99'
assert(run_program(program)[1] == '1125899906842624')

program = '109,-1,4,1,99'
assert(run_program(program)[1] == '-1')

program = '109,-1,104,1,99'
assert(run_program(program)[1] == '1')

program = '109,-1,204,1,99'
assert(run_program(program)[1] == '109')

program = '109,1,9,2,204,-6,99'
assert(run_program(program)[1] == '204')

program = '109,1,109,9,204,-6,99'
assert(run_program(program)[1] == '204')

program = '109,1,209,-1,204,-106,99'
assert(run_program(program)[1] == '204')

program = '109,1,3,3,204,2,99'
assert(run_program(program,87)[1] == '87') 

program = '109,1,203,2,204,2,99'
assert(run_program(program,888)[1] == '888')


input = get_input(sys.argv[1])
print(run_program(input,1))


