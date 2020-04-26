import sys

def get_input(file_input):
    input = []
    with open(file_input) as f:
        tmp = f.read()
        input = tmp.split()
    return input


def get_sum(input):
    sum = 0
    for d in input:
        print(d)
        i = int(d)
        sum += i
    print(sum)


input = get_input(sys.argv[1])
get_sum(input)

