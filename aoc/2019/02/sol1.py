import sys
import math

def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


def parse(codes,is1202=False):
    incs = codes.split(',')
    for i in range(0,len(incs)):
        incs[i] = int(incs[i])
    if is1202:
        incs[1] = 12
        incs[2] = 2

    i = 0
    while True:
        code = incs[i]
        if code == 99:
            break
        addr1 = incs[i+1]
        addr2 = incs[i+2]
        trgt  = incs[i+3]
        if code == 1:
            incs[trgt] = incs[addr1] + incs[addr2]
        if code == 2:
            incs[trgt] = incs[addr1] * incs[addr2]
        i = i + 4
    for i in range(0,len(incs)):
        incs[i] = str(incs[i])
    return ','.join(incs)


test = '1,9,10,3,2,3,11,0,99,30,40,50'
assert(parse(test)=='3500,9,10,70,2,3,11,0,99,30,40,50')
assert(parse('1,0,0,0,99')=='2,0,0,0,99')
assert(parse('2,3,0,3,99')=='2,3,0,6,99')
assert(parse('2,4,4,5,99,0')=='2,4,4,5,99,9801')
assert(parse('1,1,1,4,99,5,6,0,99')=='30,1,1,4,2,5,6,0,99')

input = get_input(sys.argv[1])
print(parse(input,True))


