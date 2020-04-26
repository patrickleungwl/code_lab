import sys
import math

def get_input(file):
    input = [] 
    with open(file) as f:
        tmp = f.read()
        input = tmp.split()
    return input


def get_map_key(x,y):
    key = '%i %i' % (x,y)
    return key


def mark_path_step(map,x,y,step):
    # map = map object
    # x,y = current location
    # expect Dxx 
    # where D in R,U,L,D
    # xx is a number
    dir = step[0]
    dist = step[1:]
    ndist = int(dist)

    dx = 0
    dy = 0
    if dir == 'U':
        dy = dy - 1
    if dir == 'D':
        dy = dy + 1
    if dir == 'R':
        dx = dx + 1
    if dir == 'L':
        dx = dx - 1

    while ndist>0:
        y = y + dy
        x = x + dx
        key = get_map_key(x,y)
        map[key] = 1 
        ndist = ndist -1 

    return (map,x,y)



def mark_path(path):
    x = 0
    y = 0
    map = {}
    steps = path.split(',')
    for st in steps:
        (map,x,y) = mark_path_step(map,x,y,st)
    return map 


def distance(point):
    coord = point.split(' ')
    x = abs(int(coord[0]))
    y = abs(int(coord[1]))
    return x+y


def intersections(mapa,mapb):
    points=[]
    dists=[]
    for a in mapa.keys():
        if a in mapb:
            dist = distance(a)
            dists.append(dist)
    print(sorted(dists))
            


mapa = mark_path('R75,D30,R83,U83,L12,D49,R71,U7,L72')
mapb = mark_path('U62,R66,U55,R34,D71,R55,D58,R83')
intersections(mapa,mapb)


input = get_input(sys.argv[1])
mapa = mark_path(input[0])
mapb = mark_path(input[1])
intersections(mapa,mapb)


