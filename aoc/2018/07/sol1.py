import sys
import math
import numpy as np
import datetime 

def get_input(file_input):
    coords = []
    tmp = ' '
    with open(file_input) as f:
        while tmp:
            tmp = f.readline()
            if len(tmp)<2:
                continue
            txt = tmp.split(' ')
            left = txt[1]
            right = txt[7]
            coords.append( (left, right) )
    return coords


def build_map(coords):
    map = {}
    for c in coords:
        left = c[0]
        right = c[1]
        if not left in map:
            map[left] = []
        needthese = map[left]
        needthese.append(right)
    return map


def print_map(map):
    for tobuildthis,dependencies in map.items():
        print(tobuildthis)
        for dep in dependencies:
            print('need ' + dep)



def get_root(map):
    allnodes = map.keys()
    alldeps = {}
    dependencies = map.values()
    for deps in dependencies:
        for d in deps:
            alldeps[d] = 1
    alldepskeys = alldeps.keys()

    # now which node in tobuildthis is not in alldeps?
    for nd in allnodes:
        if not nd in alldepskeys:
            return nd
    
    return '.'


def get_route(path_options):
    # given a list of options
    # choose the smallest alphabet
    chosen = min(path_options)
    return chosen


def navigate(map):
    root = get_root(map)
    path_options = ''
    path = root
    cur_node = root
    num_nodes = len(map.keys())
    while len(path)<num_nodes:
        # get list of options
        deps = map[cur_node]
        for d in deps:
            path_options = path_options + d
        print('options ' + path_options)
        cur_node = get_route(path_options)
        print('choose ' + cur_node)
        print('after options ' + path_options) 
        path_options = path_options.replace(cur_node,'')
        path = path + cur_node
    return path



# need a map of hierarchies
# to build C
#      you need A and F
#   map[C] = list(A,F)
#   map[A] = list(B,D) 
#

coords = get_input(sys.argv[1])
print(coords)
map = build_map(coords)
print_map(map)
print(navigate(map))

