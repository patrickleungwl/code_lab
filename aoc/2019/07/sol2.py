import sys
import math
import itertools

class Amplifier:
    def __init__(self,input_str,debug_mode=False):

        # cache of codes
        self.codes = self.split_string(input_str)
        
        # instruction pointer
        self.idx   = 0      

        self.debug = debug_mode


    # -----------------------------------------------------
    # set_debug
    # 

    def set_debug(self,debug_mode):
        self.debug = debug_mode

    
    # -----------------------------------------------------
    # combine_codes
    #
    # given:    an array of integers
    # returns:  a comma delmited string of integers

    def combine_codes(self):
        msg = ''
        for i in range(0,len(self.codes)):
            msg += '%i' % self.codes[i]
            if i < len(self.codes)-1:
                msg += ','
        return msg

    # -----------------------------------------------------
    # get_codes
    #

    def get_codes(self):
        return self.combine_codes()

    # -----------------------------------------------------
    # split_string
    #
    # convert comma delimited string
    # to an array of codes
    #

    def split_string(self,input):
        codes = input.split(',')
        for i in range(0,len(codes)):
            codes[i] = int(codes[i])
        return codes 

    # -----------------------------------------------------
    # get_instruction
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

    def get_instruction(self):
        code = self.codes[self.idx]
        code_str = '%05i' % (code)
        opcode = int(code_str[3:])
        pm1 = int(code_str[2])
        pm2 = int(code_str[1])
        pm3 = int(code_str[0])
        self.show_msg('code at %i = [%i %i %i %i]' % (self.idx, opcode, pm1, pm2, pm3))
        return (opcode,pm1,pm2,pm3)


    # get_param_value
    #  idx = code address
    #  pm  = param mode
    # 
    #  0, position mode
    #  1, immediate mode
    #  2, position mode
    #

    def get_param_value(self,idx,pm):
        if pm == 0:
            addr = self.codes[idx]
            return self.codes[addr]
        if pm == 1:
            return self.codes[idx]
        
        print('pm = %i' % pm)
        sys.exit(-1)


    # -----------------------------------------------------
    # debug
    # 
    # show msg if in debug mode
     
    def show_msg(self,msg):
       if self.debug==True:
           print(msg)

    # -----------------------------------------------------
    # execute
    #
    # given 
    #   idx   = the current location
    # return
    #   array of instructions [1,a,b,c]
    #   location of next idx
    #
    # 99 - stop
    # 1,a,b,c - read from positions a and b and store the sum in c
    # 2,a,b,c - read from positions a and b and store the product in c
    # 3,a - take input and put into position a
    # 4,a - take a and send to output
    # 5,a,b - if a != 0, then set IP to b
    # 6,a,b - if a == 0, then set IP to b
    # 7,a,b,c - if a < b, then put 1 into c, else put 0 into c
    # 8,a,b,c - if a == b, then put 1 into c, else put 0 into c
    #
    # Parameter modes-
    #  ABCDE
    #   1002
    # C = 1st parameter mode = 0, position mode
    # D = 2nd parameter mode = 1, immediate mode
    # E = 3rd parameter mode = 2, position mode
    #
    # 0 = position mode
    # 1 = immediate mode
    # 2 = position mode
    #
    # This function should run until 
    #  the next instruction requires an input
    #  the instruction returns an output
    #  instruction exits- 99

    def execute(self,input_value=-100):

        opcodes = [1,2,5,6,7,8]
        self.show_msg(self.get_codes())
       
        while True:
            (opcode,pm1,pm2,pm3) = self.get_instruction()
            
            if opcode == 99:
                return (0,0)

            if opcode == 3 or opcode == 4:

                # 3,a - take input and put into position a
                if opcode == 3:

                    # PL20200629 If input is blank, return -1 to tell caller
                    # to send an input value- 
                    if input_value == -100:
                        self.show_msg('Require value at %i' % self.idx)
                        return (-8,-8)

                    param1 = self.codes[self.idx+1]
                    self.show_msg('Using value of %i at %i to storage %i' % (input_value,self.idx,param1))
                    self.codes[param1] = input_value
                    input_value = -100    # input is only used once
                    self.idx += 2
                    continue

                # 4,a - take a and send to output
                if opcode == 4:
                    param1 = self.get_param_value(self.idx+1,pm1)
                    self.show_msg('opcode 4, param1 = %i' % param1)
                    self.idx += 2
                    return (1,param1)


            if opcode in opcodes:
                param1 = self.get_param_value(self.idx+1,pm1)
                param2 = self.get_param_value(self.idx+2,pm2)
                param3 = self.codes[self.idx+3]

                if opcode == 1:
                    total = param1 + param2
                    self.codes[param3] = total
                    self.idx += 4
                    msg = 'op1: p1=%i p2=%i p3=%i idx=%i' % (param1, param2, param3, self.idx)
                    self.show_msg(msg)
                    self.show_msg(self.get_codes())
                    continue

                if opcode == 2:
                    total = param1 * param2
                    self.codes[param3] = total
                    self.idx += 4
                    msg = 'op2: p1=%i p2=%i p3=%i idx=%i' % (param1, param2, param3, self.idx)
                    self.show_msg(msg)
                    self.show_msg(self.get_codes())
                    continue

                if opcode == 7:
                    self.codes[param3] = 0
                    if param1 < param2:
                        self.codes[param3] = 1
                    self.idx += 4
                    continue

                if opcode == 8:
                    self.codes[param3] = 0
                    if param1 == param2:
                        self.codes[param3] = 1
                    self.idx += 4
                    continue
            
                if opcode == 5:
                    self.idx += 3
                    if param1 != 0:
                        self.idx = param2
                    continue

                if opcode == 6:
                    self.idx += 3
                    if param1 == 0:
                        self.idx = param2
                    continue

        return (0,0)   


# --------------------------------------------------------------------------

def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


def get_all_phases_combinations():
    allphases = []

    pm = itertools.permutations('56789')
    for p in pm:
        phases = []
        for i in range(0,len(p)):
            num = int(p[i])
            phases.append(num)
        allphases.append(phases)
    return allphases


def test(input,expected_output,input_value=-1):
    amp = Amplifier(input)
    amp.execute(input_value)
    assert(amp.get_codes() == expected_output)

def test_check_stdout(input,input_value=-1,expected_stdout=-1,debug=False):
    amp = Amplifier(input,debug)
    results = amp.execute(input_value)
    assert(results[1] == expected_stdout)



# --------------------------------------------------------------------------
# Tests

assert(Amplifier("104,10,20,30,40").get_instruction() == (4,1,0,0))
assert(Amplifier("99,10,20,30,40").get_instruction() == (99,0,0,0))

test('1002,4,3,4,33','1002,4,3,4,99')
test('1,0,0,0,99','2,0,0,0,99')
test('2,3,0,3,99','2,3,0,6,99')
test('2,4,4,5,99,0','2,4,4,5,99,9801')
test('1,1,1,4,99,5,6,0,99','30,1,1,4,2,5,6,0,99')

test('3,0,99','88,0,99',88)
test_check_stdout('4,2,99',0,99)
test('1101,100,-1,4,0','1101,100,-1,4,99')

# using position mode, if input is equal to 8, output 1 else 0
test_check_stdout('3,9,8,9,10,9,4,9,99,-1,8',1,0)
test_check_stdout('3,9,8,9,10,9,4,9,99,-1,8',8,1)

# using position mode, if input is less than 8, output 1 else 0
test_check_stdout('3,9,7,9,10,9,4,9,99,-1,8',7,1)
test_check_stdout('3,9,7,9,10,9,4,9,99,-1,8',8,0)

# using immediate mode, if input is equal to 8, output 1 else 0
test_check_stdout('3,3,1108,-1,8,3,4,3,99',1,0)
test_check_stdout('3,3,1108,-1,8,3,4,3,99',8,1)

# using immediate mode, if input is less than 8, output 1 else 0
test_check_stdout('3,3,1107,-1,8,3,4,3,99',1,1)
test_check_stdout('3,3,1107,-1,8,3,4,3,99',8,0)

# if input is 0, then output 0; else output 1
test_check_stdout('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',0,0)
test_check_stdout('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',1,1)
test_check_stdout('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',8,1)
test_check_stdout('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9',-1,1)

# if input is 0, then output 0; else output 1
test_check_stdout('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',0,0)
test_check_stdout('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',1,1)
test_check_stdout('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',8,1)
test_check_stdout('3,3,1105,-1,9,1101,0,0,12,4,12,99,1',-2,1)

# if input is less than 8, output 999
# if input is 8, output 1000
# if input is greater than 8, output 1001
large_test = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
large_test = large_test + '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,'
large_test = large_test + '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'

test_check_stdout(large_test,7,999)
test_check_stdout(large_test,8,1000)
test_check_stdout(large_test,9,1001)

# --------------------------------------------------------------------------
# run_thruster
#

def run_thruster(input_str,phases):
    output = 0
    for ph in phases:
        amp = Amplifier(input_str,False)
        result = amp.execute(ph)
        if result[0] == -8:
            result = amp.execute(output)
        output = result[1]
    return output

input = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
phases = [4,3,2,1,0]
assert(run_thruster(input,phases)==43210)

input = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
phases = [0,1,2,3,4]
assert(run_thruster(input,phases)==54321)

input = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
phases = [1,0,4,3,2]
assert(run_thruster(input,phases)==65210)


# --------------------------------------------------------------------------
# run_feedback_thruster
#

def run_feedback_thruster(input_str,phases):
    # setup amps
    amps = []
    for i in range(0,5):
        amp = Amplifier(input_str,False)
        result = amp.execute(phases[i])
        amps.append(amp)
    output = 0
    while True:
        for i in range(0,5):
            amp = amps[i]
            result = amp.execute(output)
            if result[0] == 0:
                return output
            output = result[1]

input = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
phases = [9,8,7,6,5]
assert(run_feedback_thruster(input,phases)==139629729)

input = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,'
input += '-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,'
input += '53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
phases = [9,7,8,5,6]
assert(run_feedback_thruster(input,phases)==18216)


# try every combination of 5-9
# get the max thrust output from the 5 amps
max_thrust = -1
allphases = get_all_phases_combinations()

input = get_input('input.txt')
for phases in allphases:
    thrust = run_feedback_thruster(input,phases)
    print('%i at %s' % (thrust,phases))
    if thrust > max_thrust:
        max_thrust = thrust
        print('max %i at %s' % (thrust,phases))




