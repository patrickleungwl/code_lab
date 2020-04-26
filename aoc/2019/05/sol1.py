import sys
import math

def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


def get_digits(number):
    digits = []
    str = '%i' % (number)
    for i in range(len(str),0,-1):
        digits = int(str[i-1])
        digits.append(digit)
    return digits


def get_opcode(number):
# 1002
# the rightmost 2 digits is the opcode
    righttwo = number[-2:]
    return int(righttwo)


def get_code(number):
# 1002
#   first param- 0 position mode
#   secon param- 1 immediate mode
#   third param- 0 position mode
    num = int(number)
    tmp = '%05i' % (num)

    code = int(tmp[3:])
    m1mode = int(tmp[2])
    m2mode = int(tmp[1])
    m3mode = int(tmp[0])
    return (code, m1mode, m2mode, m3mode)




def parse(codes,input1):
    incs = codes.split(',')
    for i in range(0,len(incs)):
        incs[i] = int(incs[i])

    i = 0
    while True:
        code = incs[i]
        if code == 99:
            break
        (code,m1,m2,m3) = get_code(code)
      
        addr1 = 0
        addr2 = 0
        val1 = 0
        val2 = 0
        # if m1 is in position mode
        if m1 == 0:
            addr1 = incs[i+1]
            val1  = incs[addr1]
        # if m1 is in immediate mode
        if m1 == 1:
            val1 = incs[i+1]

        # if m2 is in position mode
        if m2 == 0:
            addr2 = incs[i+2]
            val2  = incs[addr2]
        # if m2 is in immediate mode
        if m2 == 1:
            val2 = incs[i+2]

        if code < 3:
            if m3 == 1:
                print('WARNING!')
                sys.exit(0)

        if code == 1:
            trgt  = incs[i+3]
            result = val1 + val2
            incs[trgt] = result
            i = i + 4
        if code == 2:
            trgt  = incs[i+3]
            result = val1 * val2
            incs[trgt] = result
            i = i + 4
        if code == 3:
            incs[addr1] = input1
            i = i + 2
        if code == 4:
            tmp = incs[addr1]
            print(tmp)
            i = i + 2
    #print('%i' % (incs[0]))
    return incs[0]


assert(get_opcode('1002')==2)
(c,m1,m2,m3) = get_code('1002')
assert(c==2)
assert(m1==0)  # position mode
assert(m2==1)  # immediate mode
assert(m3==0)

assert(get_opcode('00103')==3)
(c,m1,m2,m3) = get_code('00103')
assert(c==3)
assert(m1==1) 
assert(m2==0)
assert(m3==0)

assert(parse('3,0,99',1)==1)
assert(parse('3,0,4,0,99',1)==1)
parse('1002,4,3,4,33',1)

#input = get_input(sys.argv[1])
#parse(input,1)
#parse('1002,4,3,4,33',1)


