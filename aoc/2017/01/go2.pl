# Now, instead of considering the next digit, it wants you to
# consider the digit halfway around the circular list. That is,
# if your list contains 10 items, only include a digit in your sum
# if the digit 10/2 = 5 steps forward matches it. Fortunately,
# your list has an even number of elements.
#
#For example:
#
#  1212 produces 6: the list contains 4 items, and all four digits
#     match the digit 2 items ahead.
#  1221 produces 0, because every comparison is between a 1 and a 2.
#  123425 produces 4, because both 2s match each other, but no other
#   digit has a match.
#  123123 produces 12.
#  12131415 produces 4.


import sys

if len(sys.argv)==1:
    print('go2.pl inputstr')
    sys.exit(-1)



def get_sum(input):
    maxlength = len(input)
    lookahead = int(maxlength/2)
    cur = 0
    total = 0
    while cur < maxlength:
        ncur = cur+lookahead
        if ncur >= maxlength:
            ncur = ncur-maxlength
        ch = input[cur]
        nch = input[ncur]
        if ch == nch:
            total = total + int(ch)
        cur = cur+1
    return total



def get_input(file_input):
    input = ""
    with open(file_input) as f:
        input = f.read()
    return input

print(get_sum("1212"))      # expect 6
print(get_sum("1221"))      # expect 0
print(get_sum("123425"))    # expect 4
print(get_sum("123123"))    # expect 12
print(get_sum("12131415"))  # expect 4

input = get_input(sys.argv[1])
print(get_sum(input))

