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


def mark_path_step(map,nsteps,pathdist,x,y,step):
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
        pathdist = pathdist + 1
        if key not in nsteps:
            nsteps[key] = pathdist
        ndist = ndist - 1 
    return (map,nsteps,pathdist,x,y)


def mark_path(path):
    x = 0
    y = 0
    pathdist = 0
    map = {}
    nsteps = {}
    steps = path.split(',')
    for st in steps:
        (map,nsteps,pathdist,x,y) = mark_path_step(map,nsteps,pathdist,x,y,st)
    return (map,nsteps) 


def distance(point):
    coord = point.split(' ')
    x = abs(int(coord[0]))
    y = abs(int(coord[1]))
    return x+y


def intersections(mapa,mapb):
    points=[]
    for a in mapa.keys():
        if a in mapb:
            points.append(a) 
    return points


def min_distance(points,nstepsa,nstepsb):
    distances = []
    for p in points:
        dista = nstepsa[p]
        distb = nstepsb[p]
        dist = dista + distb
        distances.append(dist)
    return min(distances)


#(mapa,nstepsa) = mark_path('R8,U5,L5,D3')
#(mapb,nstepsb) = mark_path('U7,R6,D4,L4')
#points = intersections(mapa,mapb)
#print(distance(points,nstepsa,nstepsb))
#
(mapa,nstepsa) = mark_path('R75,D30,R83,U83,L12,D49,R71,U7,L72')
(mapb,nstepsb) = mark_path('U62,R66,U55,R34,D71,R55,D58,R83')
points = intersections(mapa,mapb)
print(min_distance(points,nstepsa,nstepsb))


(mapa,nstepsa) = mark_path('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51')
(mapb,nstepsb) = mark_path('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
points = intersections(mapa,mapb)
print(min_distance(points,nstepsa,nstepsb))

input = get_input(sys.argv[1])
(mapa,nstepsa) = mark_path(input[0])
(mapb,nstepsb) = mark_path(input[1])
points = intersections(mapa,mapb)
print(min_distance(points,nstepsa,nstepsb))


