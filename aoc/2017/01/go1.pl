# The captcha requires you to review a sequence of digits
# (your puzzle input) and find the sum of all digits that
# match the next digit in the list. The list is circular,
# so the digit after the last digit is the first digit in the list.
#
# For example:
#
#    1122 produces a sum of 3 (1 + 2) because the first digit (1)
#       matches the second digit and the third digit (2) matches the 
#       fourth digit.
#    1111 produces 4 because each digit (all 1) matches the next.
#    1234 produces 0 because no digit matches the next.
#    91212129 produces 9 because the only digit that matches the
#       next one is the last digit, 9.

import sys


if len(sys.argv)==1:
    print('go.pl inputstr')
    sys.exit(-1)


def get_sum(input):
    maxlength = len(input)
    cur = 0
    total = 0
    while cur < maxlength:
        ncur = cur+1
        if ncur >= maxlength:
            ncur = 0
        ch = input[cur]
        nch = input[ncur]
        if ch == nch:
            total = total + int(ch)
            #print('%s %s' % (ch, total))
        cur = cur+1
    return total


def get_input(file_input):
    input = ""
    with open(file_input) as f:
        input = f.read()
    return input


# run initial tests
print(get_sum("1122"))      # expect 3
print(get_sum("1111"))      # expect 4
print(get_sum("1234"))      # expect 0
print(get_sum("91212129"))  # expect 9
    
input = get_input(sys.argv[1])
print(get_sum(input))

