

def get_digits(number):
    digits = []
    str = '%i' % (number)
    for i in range(len(str),0,-1):
        digit = int(str[i-1])
        digits.append(digit)
    return digits


# let's pick a target candidate for adj digits
# if candidate have exactly 2 digits, then it works
# if candidate have more than 2 digits in sequence, 
# then it's no good
# so let's just scan digits 0-9 one at a time

def same_adjacent_digits(digits):
    #print(digits)
    for d in range(0,10):
        num_adj = 1
        #print('checking number %i' % (d))
        for i in range(0,len(digits)-1):
            left = digits[i]
            right = digits[i+1]
            #print('%i %i' % (left, right))
            if left == right and left==d:
                num_adj = num_adj + 1
                #print(' num_adj=%i' % (num_adj))
        #print('number %i has %i adj' % (d, num_adj))
        if num_adj == 2:
            return True
    return False



def increasing_digits(digits):
    i = 0
    while i<len(digits)-1:
        left = digits[i]
        right = digits[i+1]
        if right > left:
            return False
        i = i + 1
    return True


# tests
assert(same_adjacent_digits(get_digits(991234)))
assert(same_adjacent_digits(get_digits(123499)))
assert(not same_adjacent_digits(get_digits(999123)))
assert(not same_adjacent_digits(get_digits(123999)))
assert(same_adjacent_digits(get_digits(111899)))
assert(same_adjacent_digits(get_digits(222699)))
assert(same_adjacent_digits(get_digits(993333)))
assert(same_adjacent_digits(get_digits(889922)))
assert(same_adjacent_digits(get_digits(121122)))
assert(not same_adjacent_digits(get_digits(132221)))
assert(same_adjacent_digits(get_digits(111122)))
assert(same_adjacent_digits(get_digits(132122)))
assert(same_adjacent_digits(get_digits(112231)))
assert(not same_adjacent_digits(get_digits(122221)))
assert(not same_adjacent_digits(get_digits(122231)))
assert(same_adjacent_digits(get_digits(224444)))

digits = get_digits(122345)
assert(digits[0]==5)
assert(digits[5]==1)

assert(same_adjacent_digits(digits))
assert(increasing_digits(digits))

digits = get_digits(128345)
assert(not same_adjacent_digits(digits))
assert(not increasing_digits(digits))

assert(same_adjacent_digits(get_digits(112233)))
assert(not same_adjacent_digits(get_digits(123444)))
assert(same_adjacent_digits(get_digits(111122)))

start = 138307
end = 654504
num_possible = 0
for number in range(start,end):
    digits = get_digits(number)
    if same_adjacent_digits(digits) and increasing_digits(digits):
        num_possible = num_possible + 1
print(num_possible)

