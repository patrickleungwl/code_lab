import sys
import numpy as np

def get_input(file_input):
    input = []
    with open(file_input) as f:
        tmp = f.read()
        input = tmp.split('\n')
    return input


def parse_input(area_def):
    # parse #1 @ 146,196: 19x14
    print(area_def)
    defs = area_def.split()
    xy_raw = defs[2]
    xy = xy_raw[:-1]
    xys = xy.split(',')
    size_raw = defs[3]
    sizexy = size_raw.split('x')
    x = int(xys[0])
    y = int(xys[1])
    dx = int(sizexy[0])
    dy = int(sizexy[1])
    return (x,y,dx,dy)


def is_clean_claim(x,y,dx,dy):
    for row in range(y,y+dy):
        for col in range(x,x+dx):
            val = fabric[row,col]
            # if square is overlapped, this is not the
            # clean claim
            if val > 1:
                return False
    return True


def find_nooverlapped_claim(input):
    for i, area_def in enumerate(input):
        if len(area_def) < 1:
            continue
        (x,y,dx,dy) = parse_input(area_def)
        if is_clean_claim(x,y,dx,dy):
            print(i+1)
            break


def count_overlapped_squares():
    nrows = fabric.shape[0]
    ncols = fabric.shape[1]
    overlapped = 0
    for row in range(0,nrows):
        for col in range(0,ncols):
            if fabric[row,col] > 1:
                overlapped = overlapped + 1
    print(overlapped)



def set_areas(input):
    for i, area_def in enumerate(input):
        if len(area_def) < 1:
            continue
        (x,y,dx,dy) = parse_input(area_def)
        for row in range(y,y+dy):
            for col in range(x,x+dx):
                val = fabric[row,col]
                val = val + 1
                fabric[row,col] = val
                claims[row,col] = i
    print(fabric)


fabric = np.zeros((1100,1100))
claims = np.zeros((1100,1100))
input = get_input(sys.argv[1])
set_areas(input)
count_overlapped_squares()
find_nooverlapped_claim(input)

