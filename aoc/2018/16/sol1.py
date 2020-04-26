import sys


#Before: [3, 2, 1, 1]
#9 2 1 2
#After:  [3, 2, 2, 1]


def get_input(file_input):
    tmp = ' '
    before_list = []
    after_list = []
    opcodes_list = []

    with open(file_input) as f:
        while tmp:
            tmp = f.readline()
            if len(tmp)<2:
                continue
            if tmp.find('Before')>-1:
                beg_idx = tmp.find('[')+1
                end_idx = tmp.find(']')
                regs = tmp[beg_idx:end_idx].split(',')
                before_regs = set_regs(int(regs[0]), int(regs[1]), int(regs[2]), int(regs[3]))
                before_list.append(before_regs)
                continue
            if tmp.find('After')>-1:
                beg_idx = tmp.find('[')+1
                end_idx = tmp.find(']')
                regs = tmp[beg_idx:end_idx].split(',')
                after_regs = set_regs(int(regs[0]), int(regs[1]), int(regs[2]), int(regs[3]))
                after_list.append(after_regs)
                continue
            # this must be opcodes
            ops = tmp.split(' ')
            opcodes = set_regs(int(ops[0]), int(ops[1]), int(ops[2]), int(ops[3]))
            opcodes_list.append(opcodes)
            

    return( before_list, opcodes_list, after_list )



def addr(regs,a,b,c):
    regs[c] = regs[a] + regs[b]

def addi(regs,a,b,c):
    regs[c] = regs[a] + b

def mulr(regs,a,b,c):
    regs[c] = regs[a] * regs[b]

def muli(regs,a,b,c):
    regs[c] = regs[a] * b

def banr(regs,a,b,c):
    regs[c] = regs[a] & regs[b]

def bani(regs,a,b,c):
    regs[c] = regs[a] & b

def borr(regs,a,b,c):
    regs[c] = regs[a] | regs[b]

def bori(regs,a,b,c):
    regs[c] = regs[a] | b

def setr(regs,a,b,c):
    regs[c] = regs[a]

def seti(regs,a,b,c):
    regs[c] = a

def gtir(regs,a,b,c):
    val = 0
    if a > regs[b]:
        val = 1
    regs[c] = val

def gtri(regs,a,b,c):
    val = 0
    if regs[a] > b:
        val = 1
    regs[c] = val

def gtrr(regs,a,b,c):
    val = 0
    if regs[a] > regs[b]:
        val = 1
    regs[c] = val

def eqir(regs,a,b,c):
    val = 0
    if a > regs[b]:
        val = 1
    regs[c] = val

def eqri(regs,a,b,c):
    val = 0
    if regs[a] > b:
        val = 1
    regs[c] = val

def eqrr(regs,a,b,c):
    val = 0
    if regs[a] > regs[b]:
        val = 1
    regs[c] = val

def set_regs(r0, r1, r2, r3):
    regs = []
    regs.append(r0)
    regs.append(r1)
    regs.append(r2)
    regs.append(r3)
    return regs


def execute_instruction(op,regs,a,b,c):
    if op == 0:
        addr(regs,a,b,c)
    if op == 1:
        addi(regs,a,b,c)
    if op == 2:
        mulr(regs,a,b,c)
    if op == 3:
        muli(regs,a,b,c)
    if op == 4:
        banr(regs,a,b,c)
    if op == 5:
        bani(regs,a,b,c)
    if op == 6:
        borr(regs,a,b,c)
    if op == 7:
        bori(regs,a,b,c)
    if op == 8:
        setr(regs,a,b,c)
    if op == 9:
        seti(regs,a,b,c)
    if op == 10:
        gtir(regs,a,b,c)
    if op == 11:
        gtri(regs,a,b,c)
    if op == 12:
        gtrr(regs,a,b,c)
    if op == 13:
        eqir(regs,a,b,c)
    if op == 14:
        eqri(regs,a,b,c)
    if op == 15:
        eqrr(regs,a,b,c)


def test_results_match(test_op,before_regs,opcodes,after_regs):
    results_match = False
    test_regs = before_regs.copy()
    execute_instruction(test_op,test_regs,test_regs[1],test_regs[2],test_regs[3])
    if test_regs == after_regs:
        results_match = True
    return results_match


before_regs = set_regs(0,1,2,3)
after_regs = set_regs(0,1,2,3)
opcodes = set_regs(13,0,0,1)

#for test_op in range(0,15):
#    print('%s %s' % (test_op,test_results_match(test_op,before_regs,opcodes,after_regs)))


(before_list, opcodes_list, after_list) = get_input(sys.argv[1])

num_samples_behaves = 0
for i in range(0,len(before_list)):
    before_regs = before_list[i]
    opcodes = opcodes_list[i]
    after_regs = after_list[i]

    num_matches = 0
    for test_op in range(0,15):
        if test_results_match(test_op,before_regs,opcodes,after_regs):
            num_matches = num_matches + 1

    if num_matches >= 3:
        print('%s %s %s' % (before_regs, opcodes, after_regs))
        num_samples_behaves = num_samples_behaves + 1

print(num_samples_behaves)




