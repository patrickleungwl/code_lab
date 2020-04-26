import sys
import math

# mass, divide by 3, round down, subtract 2

def get_input(file):
    input = []
    with open(file) as f:
        tmp = f.read()
        input = tmp.split()
    return input

def generate_graph(input):
    orbits_ctp = {}  # child to parent
    orbits_ptc = {}  # paren to child
    for row in input:
        r = row.split(')')
        parent = r[0]
        child = r[1]
        orbits_ptc[parent] = child
        orbits_ctp[child] = parent
        print('parent %s has planet %s' % (parent, child))
    return (orbits_ctp, orbits_ptc)


def get_num_parents(orbits_ctp, child):
    num_orbits = 0
    while True:
        if child in orbits_ctp:
            child = orbits_ctp[child]
            num_orbits = num_orbits + 1
        else:
            break
    return num_orbits


def get_total_orbits(orbits_ctp):
    total = 0
    for c in orbits_ctp.keys():
        num = get_num_parents(orbits_ctp, c)
        total = total + num
    return total


input = get_input('test.txt')
(octp, optc) = generate_graph(input)
assert(get_num_parents(octp, 'B')==1)
assert(get_num_parents(octp, 'G')==2)
assert(get_num_parents(octp, 'D')==3)
assert(get_num_parents(octp, 'L')==7)
assert(get_num_parents(octp, 'COM')==0)
assert(get_total_orbits(octp) == 42)


input = get_input('input.txt')
(octp, optc) = generate_graph(input)
print(get_total_orbits(octp))

