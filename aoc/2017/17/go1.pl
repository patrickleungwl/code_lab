import sys

cache = []

# 123456789
# move ahead 12 = 12-9 = 3



def move_forward_n_steps(cache, cur_pos, n):
    if len(cache)==0:
        return 0

    for i in range(0, n):
        cur_pos = cur_pos+1
        if cur_pos >= len(cache):
            cur_pos = 0
    return cur_pos


def insert_value_after_cur_pos(cache, cur_pos, value):
    new_pos = cur_pos+1
    cache.insert(new_pos, value)
    return new_pos



if len(sys.argv)==1:
    print('go.pl steps_to_jump')
    sys.exit(-1)


cur_pos = 0
i = 0 
n = int(sys.argv[1])
while i <= 2017:
    cur_pos = move_forward_n_steps(cache, cur_pos, n)
    cur_pos = insert_value_after_cur_pos(cache, cur_pos, i)
    print('%s %s' % (i, cache))
    i = i + 1 


