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
            xy = tmp.split(',')
            x = int(xy[0].strip())
            y = int(xy[1].strip())
            coords.append( (x,y) )
    return coords



def calc_block_distance(fromx,fromy,tox,toy):
    diffx = abs(tox-fromx)
    diffy = abs(toy-fromy)
    distance = diffx+diffy
    #print('%s,%s to %s,%s => %s' % (fromx,fromy,tox,toy,distance))
    return distance

# return the number of the nearest star
# or -1 if a tie
def get_nearest_star(fromx,fromy):
    shortest_distance = 100000
    nearest_star = -100
    for i, star in enumerate(coords):
        distance = calc_block_distance(fromx,fromy,star[0],star[1])
        # if distance to this star already matches
        # distance previously calced to another star
        # then return a tie, -1
        if distance == shortest_distance:
            nearest_star = -1

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_star = i

    return (nearest_star, shortest_distance)


def get_nearest_star_for_entire_grid(grid):
    for x in range(0,grid.shape[0]):
        for y in range(0,grid.shape[1]):
            nstar = get_nearest_star(x,y)
            domain_map[x,y] = nstar[0]
            print('xy %s,%s => x%sx %s' % (x,y,nstar[0],nstar[1]))


def get_star_domain(star_num):
    # just review the grid
    # count the number of squares owned by star
    # for edge owned by star- immediately return infinite

    total_domain = 0
    for x in range(0,grid.shape[0]):
        for y in range(0,grid.shape[1]):
            nstar = domain_map[x,y]
            if nstar != star_num:
                continue
            if x==0 or x==grid.shape[0]-1 or y==0 or y==grid.shape[1]-1:
                return -1
            total_domain = total_domain+1
    return total_domain


def get_star_with_biggest_domain():
    biggest_domain = -1
    biggest_star = -1
    for i, star in enumerate(coords):
        domain = get_star_domain(i)
        if domain > biggest_domain: 
            biggest_domain = domain
            biggest_star = i
    return (biggest_star,biggest_domain)


# let's imagine a grid
# for each point, get the distance to the nearest star
# this requires calcing the distance to each star

grid = np.zeros((380,380))
domain_map = np.zeros((380,380))
coords = get_input(sys.argv[1])
print(coords)
#print(get_nearest_star(5,2))
get_nearest_star_for_entire_grid(grid)
print(get_star_with_biggest_domain())

