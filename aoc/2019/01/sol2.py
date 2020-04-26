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
    module = 0
    for i in input:
        t = get_fuel(int(i))
        total = total + t
        print('[%i] %s requires %i fuel => total %i' % (module,i,t,total))
        while True:
            t = get_fuel(t) 
            if t<=0:
                break
            total = total + t
            print('%i -> %i' % (t, total))
        module = module + 1
    return total

assert(get_fuel(12)==2)
assert(get_fuel(14)==2)
assert(get_fuel(1969)==654)
assert(get_fuel(100756)==33583)

assert(get_total_fuel_requirements(['14'])==2)
assert(get_total_fuel_requirements(['1969'])==966)
assert(get_total_fuel_requirements(['100756'])==50346)

input = get_input(sys.argv[1])
total = get_total_fuel_requirements(input)
print(total)


