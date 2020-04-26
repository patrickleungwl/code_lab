import sys
import math
import numpy as np
import datetime 

def get_input(file_input):
    tmp = ''
    with open(file_input) as f:
        tmp = f.readline()
    return tmp.strip()


# return (num of child nodes, num of metadata, last index pos)
def get_node_data(idx, level):
    cidx = input.find(' ',idx)
    if cidx == -1:
        return
    midx = input.find(' ',cidx+1)
    if midx == -1:
        return
    child = input[idx:cidx]
    metadata = input[cidx+1:midx]
    num_child = int(child)
    num_meta  = int(metadata)
    print(' ' * level + 'num_child=%s num_meta=%s pos=%s' % (num_child, num_meta, midx))
    return (num_child, num_meta, midx+1)


def get_metadata(idx, level):
    midx = input.find(' ',idx+1)
    if midx == -1:
        midx = idx+1
    metadata = input[idx:midx]
    print(' ' * level + ' metadata = %s' % (metadata))
    return (int(metadata), midx+1)


# return last idx read
def parse_tree(idx, level):
    sum_meta = 0

    # num of child nodes
    # num of metadata data
    level = level + 1
    (num_children, num_meta, idx) = get_node_data(idx, level)
    
    # for each child, drill down
    for child in range(0,num_children):
        (idx,sum_meta_from_children) = parse_tree(idx, level)
        sum_meta = sum_meta + sum_meta_from_children

    # read the metadata
    for meta in range(0,num_meta):
        (metadata, idx) = get_metadata(idx, level) 
        sum_meta = sum_meta + metadata

    return (idx,sum_meta)

sum_meta = 0
input = get_input(sys.argv[1])
(idx, sum_meta) = parse_tree(0, 0)
print(sum_meta)
