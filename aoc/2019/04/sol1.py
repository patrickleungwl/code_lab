

def get_digits(number):
    digits = []
    str = '%i' % (number)
    for i in range(len(str),0,-1):
        digit = int(str[i-1])
        digits.append(digit)
    return digits

def same_adjacent_digits(digits):
    i = 0
    while i<len(digits)-1:
        left = digits[i]
        right = digits[i+1]
        if left == right:
            return True
        i = i + 1
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

digits = get_digits(122345)
assert(digits[0]==5)
assert(digits[5]==1)

assert(same_adjacent_digits(digits))
assert(increasing_digits(digits))

digits = get_digits(128345)
assert(not same_adjacent_digits(digits))
assert(not increasing_digits(digits))

start = 138307
end = 654504
num_possible = 0
for number in range(start,end):
    digits = get_digits(number)
    if same_adjacent_digits(digits) and increasing_digits(digits):
        num_possible = num_possible + 1
print(num_possible)

