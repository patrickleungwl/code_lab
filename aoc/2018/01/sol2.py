import sys

def get_input(file_input):
    input = []
    with open(file_input) as f:
        tmp = f.read()
        input = tmp.split()
    return input


def get_sum(input):
    sum = 0
    cache = {}
    while 1:
        for d in input:
            i = int(d)
            sum += i
            print("%s .... %s" % (i, sum))
            if sum in cache:
                print("detected = %s" % sum)
                return
            cache[sum] = 1
        print("\n")

input = get_input(sys.argv[1])
get_sum(input)

