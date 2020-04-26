import sys
import math

def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


def parse(codes,inp1=0,inp2=0):
    incs = codes.split(',')
    for i in range(0,len(incs)):
        incs[i] = int(incs[i])
    if inp1>0:
        incs[1] = inp1
    if inp2>0:
        incs[2] = inp2

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
    return incs[0]


input = get_input(sys.argv[1])
for inp1 in range(0,99):
    for inp2 in range(0,99):
        result = parse(input,inp1,inp2)
        if result == 19690720:
            print(inp1,inp2,inp1*100+inp2)
            sys.exit(0)



