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


def get_new_state(state, rules):
    new_state = ''
    for idx in range(0,len(state)-3):
        if idx<2:
            new_state = new_state + '.'
            continue

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

    new_state = new_state + '...'
    return (new_state)


def count_plants(state,start_idx):
    num = 0
    for i in range(0,len(state)):
        if state[i]=='#':
            num = num+i-start_idx
    return num


#state = '#..#.#..##......###...###' 
state = '#.#####.##.###...#...#.####..#..#.#....##.###.##...#####.#..##.#..##..#..#.#.#.#....#.####....#..#'
state = '..........' + state + '.' * 2000
rules = get_input(sys.argv[1])
start_idx = 10
print('%s %s' % (0,state))
for n in range(1,1001):
    state = get_new_state(state, rules)
    num = count_plants(state, start_idx)
    print('%s %s   %s' % (n,state,num))

