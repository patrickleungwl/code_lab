import sys


def get_input(file_input):
    rules = {}

    tmp = ' '
    with open(file_input) as f:
        while len(tmp)>0: 
            tmp = f.readline()
            start = tmp[0:6].strip()
            end   = tmp[9:].strip()
            rules[start] = end
    return rules


def get_new_state(state, rules, start_idx):
    state = '....' + state + '....'
    start_idx = start_idx + 4
    new_state = ''
    for idx in range(2,len(state)):
        region = state[idx-2:idx+3]
        #print('Comparing ' + region)
        if region in rules:
            next_gen = rules[region]
            #print('Hit rule to ' + next_gen)
        else:
            next_gen = '.'
            #print('Default to ' + next_gen)
        new_state = new_state + next_gen 
        #print('%s: %s' % (idx,new_state))

    # clean up left and right states
    if new_state[:5] == '.....':
        new_state = new_state[5:]
        start_idx = start_idx - 4
    if new_state[len(new_state)-5:] == '.....':
        new_state = new_state[:len(new_state)-5]

    return (new_state,start_idx)


def count_plants(state, start_idx):
    num = 0
    for i in range(0,len(state)):
        if state[i]=='#':
            num = num+1
    return num


state = '#..#.#..##......###...###' 
rules = get_input(sys.argv[1])
total_plants = 0
    
print('%s %s' % (0,state))
start_idx = 0
for n in range(1,21):
    (state, start_idx) = get_new_state(state, rules, start_idx)
    num = count_plants(state, start_idx)
    total_plants = total_plants + num
    print('%s %s   %s %s' % (n,state,num,total_plants))
print(total_plants)

