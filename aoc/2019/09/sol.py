import sys
import math
import itertools

class Amplifier:
    def __init__(self,input_str,debug_mode=False):

        # cache of codes
        self.codes = self.split_string(input_str)
        
        # instruction pointer
        self.idx   = 0      

        # relative base
        self.relative_base = 0

        # debug printing
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
    # get_debug_codes
    #

    def get_debug_codes(self,count):
        msg = ''
        max_cell = len(self.codes)-1
        # find first non zero
        for maxc in range(max_cell,0,-1):
            if self.codes[maxc]!=0:
                break
        for i in range(0,maxc+1):
            msg += '%i.%i:%i\n' % (count,i,self.codes[i])
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
        #for i in range(len(codes),100*len(codes)):
        #    codes.append(0)
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
    # B = 2nd parameter mode = 1, immediate mode
    #
    #
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


    def extend_code_space(self,addr):
        limit = addr+10
        #if limit < len(self.codes)*10:
        #    limit = len(self.codes)*10
        for i in range(len(self.codes),limit):
            self.codes.append(0)


    # get_param_value
    #  idx = code address
    #  pm  = param mode
    # 
    #  0, position mode
    #  1, immediate mode
    #  2, relative mode
    #
    # 203 0 means op3, take the input and put into 
    #  address pointed to by the first parameter, relative mode
    #  meaning 0 + relativebase
    # 

    def get_param_value(self,idx,pm):
        addr = -1
        msg = 'get_param_value '
        if pm == 0:
            addr = self.codes[idx]
            msg += 'mode 0, get value at address in idx %i => %i' % (idx,addr)
        if pm == 1:
            addr = idx
            msg += 'mode 1, get value in idx %i' % (idx)
        if pm == 2:
            addr = self.codes[idx]
            addr += self.relative_base
            msg += 'mode 2, get value in address %i from base %i + addr in idx %i, %i' % (addr, self.relative_base, idx, self.codes[idx])

        if addr > len(self.codes):
            self.extend_code_space(addr)

        msg += ' ==> %i' % (self.codes[addr])
        self.show_msg(msg)

        return self.codes[addr]



    # -----------------------------------------------------
    # debug
    # 
    # show msg if in debug mode
     
    def show_msg(self,msg):
        if self.debug==True:
            print('DEBUG:' + msg)

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
        #self.show_msg(self.get_codes())
       
        count = 0
        while True:
            if count < 100:
                #print(self.get_debug_codes(count))
                count += 1

            (opcode,pm1,pm2,pm3) = self.get_instruction()
            
            if opcode == 99:
                return (0,0)

            if opcode == 9:
                param1 = self.get_param_value(self.idx+1,pm1)
                self.relative_base += param1
                self.idx += 2

                msg = 'op9: add p1=%i to base; new relative_base=%i idx=%i; ' % (param1, self.relative_base, self.idx)
                self.show_msg(msg)
                continue

            if opcode == 3 or opcode == 4:

                # 3,a - take input and put into position a
                # 203 0 means op3, take the input and put into 
                #  address pointed to by the first parameter, relative mode
                #  meaning 0 + relativebase
                if opcode == 3:
                    self.show_msg('op3 %i %i' % (self.codes[self.idx],self.codes[self.idx+1]))

                    # PL20200629 If input is blank, return -1 to tell caller
                    # to send an input value- 
                    if input_value == -100:
                        self.show_msg('Require value at %i' % self.idx)
                        return (-8,-8)
                    
                    msg = ''
                    if pm1 == 2:
                        addr = self.codes[self.idx+1]
                        addr += self.relative_base
                        self.codes[addr] = input_value
                        msg = 'op3: addr=%i input=%i; put input value into addr' % (addr, input_value)
                    else:
                        # always mode 1, there can be no mode 0 for op3
                        param1 = self.get_param_value(self.idx+1,1)
                        msg = 'op3: addr=%i input=%i; put input value into addr' % (param1, input_value)
                        self.codes[param1] = input_value
                    self.idx += 2

                    self.show_msg(msg)
                    
                    input_value = -100    # input is only used once
                    continue

                # 4,a - take a and send to output
                if opcode == 4:
                    param1 = self.get_param_value(self.idx+1,pm1)
                    self.idx += 2

                    msg = 'op4: p1=%i idx=%i; output p1' % (param1, self.idx)
                    self.show_msg(msg)

                    return (1,param1)


            if opcode in opcodes:
                param1 = self.get_param_value(self.idx+1,pm1)
                param2 = self.get_param_value(self.idx+2,pm2)
                #param3 = self.codes[self.idx+3]

                # output param is always position mode
                if pm3 == 2:
                    param3 = self.codes[self.idx+3]
                    param3 += self.relative_base
                else:
                    param3 = self.get_param_value(self.idx+3,1)

                if param3 > len(self.codes):
                    self.extend_code_space(param3)

                if opcode == 1:
                    total = param1 + param2
                    self.codes[param3] = total
                    self.idx += 4

                    msg = 'op1: p1=%i p2=%i p3=%i total=%i idx=%i; add p1 and p2, put total in p3 ' % (param1, param2, param3, total, self.idx)
                    self.show_msg(msg)
                    continue

                if opcode == 2:
                    total = param1 * param2
                    self.codes[param3] = total
                    self.idx += 4

                    msg = 'op2: p1=%i p2=%i p3=%i total=%i idx=%i; multiply p1 and p2, put total in p3 ' % (param1, param2, param3, total, self.idx)
                    self.show_msg(msg)
                    continue

                if opcode == 7:
                    self.codes[param3] = 0
                    if param1 < param2:
                        self.codes[param3] = 1
                    self.idx += 4

                    msg = 'op7: p1=%i p2=%i p3=%i idx=%i; if p1<p2 set p3 to 1' % (param1,param2,param3,self.idx)
                    self.show_msg(msg)
                    continue

                if opcode == 8:
                    self.codes[param3] = 0
                    if param1 == param2:
                        self.codes[param3] = 1
                    self.idx += 4

                    msg = 'op8: p1=%i p2=%i p3=%i idx=%i; if p1=p2 set p3 to 1' % (param1,param2,param3,self.idx)
                    self.show_msg(msg)
                    continue
            
                if opcode == 5:
                    self.idx += 3
                    if param1 != 0:
                        self.idx = param2

                    msg = 'op5: p1=%i p2=%i idx=%i; if p1<>0 set idx to p2' % (param1,param2,self.idx)
                    self.show_msg(msg)
                    continue

                if opcode == 6:
                    self.idx += 3
                    if param1 == 0:
                        self.idx = param2

                    msg = 'op6: p1=%i p2=%i idx=%i; if p1=0 set idx to p2' % (param1,param2,self.idx)
                    self.show_msg(msg)
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
    amp = Amplifier(input,False)
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

test_check_stdout('4,2,99',0,99)
test('1101,100,-1,4,0','1101,100,-1,4,99')
test('3,0,4,0,99','88,0,4,0,99',88)

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
# Test relative mode

def test_day9_extensions(input):
    amp = Amplifier(input)
    while True:
        result = amp.execute(0)
        if result[0]==0:
            break


input = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
test_day9_extensions(input)

input = '1102,34915192,34915192,7,4,7,99,0'
test_day9_extensions(input)

input = '104,1125899906842624,99'
test_day9_extensions(input)

# --------------------------------------------------------------------------
# Run day9 problem for real

def test_day9_for_real(input):
    input_txt = get_input('input.txt')
    amp = Amplifier(input_txt,False)
    while True:
        result = amp.execute(input)
        print(result)
        if result[0]==0:
            break

print('testing day9, part 1')
test_day9_for_real(1)

print('testing day9, part 2')
test_day9_for_real(2)


