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
    parents = []
    while True:
        if child in orbits_ctp:
            child = orbits_ctp[child]
            num_orbits = num_orbits + 1
            parents.append(child)
        else:
            break
    return (num_orbits,parents)


def get_total_orbits(orbits_ctp):
    total = 0
    for c in orbits_ctp.keys():
        (num,parents) = get_num_parents(orbits_ctp, c)
        total = total + num
    return total




def get_common_point(orbits_ctp,a,b):
    # from a to b
    # what is the common point
     
    # get all planets to root for a
    (numa, parentsa) = get_num_parents(orbits_ctp,a)
    (numb, parentsb) = get_num_parents(orbits_ctp,b)

    # now find a and b's closet planet
    print(parentsa)
    print(parentsb)
    la = len(parentsa)
    lb = len(parentsb)
    while True:
        la = la-1
        lb = lb-1
        #print('[%i %s] [%i %s]' % (la, parentsa[la], lb, parentsb[lb]))
        if parentsa[la] != parentsb[lb]:
            break
    common = parentsa[la+1]
    #print(common)
    #print('%i %i' % (la, lb))
    #print('%i %i' % (numa, numb))
    return (la+1 + lb+1)


input = get_input('test2.txt')
(octp, optc) = generate_graph(input)
print(get_common_point(octp,'YOU','SAN'))

input = get_input('input.txt')
(octp, optc) = generate_graph(input)
print(get_common_point(octp,'YOU','SAN'))

