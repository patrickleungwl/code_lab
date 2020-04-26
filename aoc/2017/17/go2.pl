#
# 0 [0]
# 1 [0, 1]          should return 0 
#                   given [0, 1], from 1, skip 3 (0,1,0)- insert 2 after 0
#                   this means code should return 0
#
# 2 [0, 2, 1]
# 3 [0, 2, 3, 1]    starting 1, +3, len=3, 
#                   
#                  if cur_pos+jump > len, newpos = len % 3 else newpos = cur_pos+3
#                  at step 4, beginning len = 4
#                  at end of step 4, len =
# 4 [0, 2, 4, 3, 1]
# 5 [0, 5, 2, 4, 3, 1]
# 6 [0  5  2  4  3 6 1]


def move_forward_n_steps(cur_step, cur_pos, jump_size):

    if cur_step == 0:
        return -1;

    array_length = cur_step
    new_pos = cur_pos + jump_size
    while new_pos >= array_length:
        new_pos = new_pos - array_length

    return new_pos


print(move_forward_n_steps(0, -1, 3))   # expect -1
print(move_forward_n_steps(1, 0, 3))    # expect 0 before append
print(move_forward_n_steps(2, 1, 3))    # expect 0 before append
print(move_forward_n_steps(3, 1, 3))    # expect 1 before append
print(move_forward_n_steps(4, 2, 3))    # expect 1 before append
print(move_forward_n_steps(5, 2, 3))    # expect 4 before append
print('end of checks')

cur_pos = 0
i = 0
n = 382
while i<=50000000:
    cur_pos = move_forward_n_steps(i, cur_pos, n) + 1
    #print('%s %s' % (i, cur_pos-1))
    if cur_pos==1:
        print('%s %s' % (i, cur_pos-1))
    i=i+1


