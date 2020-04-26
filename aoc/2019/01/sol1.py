import sys
import math

# mass, divide by 3, round down, subtract 2

def get_input(file):
    input = []
    with open(file) as f:
        tmp = f.read()
        input = tmp.split()
    return input


def get_fuel(mass):
    m = math.floor(mass/3.0)-2
    return m

def get_total_fuel_requirements(input):
    total = 0
    for i in input:
       total = total + get_fuel(int(i))
    return total


assert(get_fuel(12)==2)
assert(get_fuel(14)==2)
assert(get_fuel(1969)==654)
assert(get_fuel(100756)==33583)


input = get_input(sys.argv[1])
total = get_total_fuel_requirements(input)
print(total)


