import numpy as np


def get_hundreds_place(num):
    if num < 100:
        return 0
    tmp = '%s' % (int(num))
    hp = tmp[-3:-2]
    return int(hp)


def calc_power_level(x,y,snum):
    rack_id = x + 10
    power_level = rack_id * y
    power_level = power_level + snum
    power_level = power_level * rack_id
    power_level = get_hundreds_place(power_level)
    power_level = power_level - 5
    return power_level


def set_power_levels_in_grid(grid,snum):
    for x in range(0,grid.shape[0]):
        for y in range(0,grid.shape[1]):
            grid[x,y] = calc_power_level(x,y,snum)


# memget_subgrid_total_power
#  1 2 3 x
#  1 2 3 x
#  1 2 3 x
#  x x x x
#
def memget_subgrid_total_power(grid,x,y,sqsize,cache):
    # look for subgrid in key first
    # if not found, look for t-1 subgrid
    # if found, get the t-1 subgrid- and add the edges
    # then store into cache
    #
    cachekey = '%s_%s_%s' % (x,y,sqsize)
    if cachekey in cache:
        return cache[cachekey]
    subkey = '%s_%s_%s' % (x,y,sqsize-1)
    total_power = 0
    if subkey in cache:
        subkey_power = cache[subkey]
        total_power = subkey_power
        for ty in range(y,y+sqsize-1):
            total_power = total_power + grid[x+sqsize-1,ty]
        for tx in range(x,x+sqsize):
            total_power = total_power + grid[tx,y+sqsize-1]
    else:
        total_power = get_subgrid_total_power(grid,x,y,sqsize)

    cache[cachekey] = total_power
    return total_power



#  1 2 3 x
#  1 2 3 x
#  1 2 3 x
#  x x x x
#

def get_subgrid_total_power(grid,x,y,sqsize):
    total = 0
    for tx in range(x,x+sqsize):
        for ty in range(y,y+sqsize):
            total = total + grid[tx,ty]
    return total


def find_max_subgrid(grid,sqsize,cache):
    max = -100    
    max_grid_location = (0,0)
    for x in range(0,grid.shape[0]-sqsize):
        for y in range(0,grid.shape[1]-sqsize):
            total = memget_subgrid_total_power(grid,x,y,sqsize,cache)
            if total > max:
                max = total
                max_grid_location = (x,y)
    return (max, max_grid_location)


def calc_all_subgrids(grid):
    max_list = []
    cache = {}
    for sqsize in range(1,297):
        print('calc_all_subgrids %s' % (sqsize))
        (max, max_grid_location) = find_max_subgrid(grid,sqsize,cache)
        max_list.append((max, max_grid_location, sqsize))
    return max_list


def find_max_subgrid_from_allsubgrids(max_list):
    max = -100
    max_grid_location = 0
    max_sqsize = 0
    for item in max_list:
        subgrid_max = item[0]
        subgrid_max_location = item[1]
        sqsize=item[2]
        if (subgrid_max > max):
            max = subgrid_max
            max_grid_location = subgrid_max_location
            max_sqsize = sqsize
    return (max, max_grid_location,max_sqsize)


assert calc_power_level(122,79,57)==-5, 'Power level test 1'
assert calc_power_level(217,196,39)==0, 'Power level test 2'
assert calc_power_level(101,153,71)==4, 'Power level test 3'

snum = 3613
grid = np.zeros((300,300))
set_power_levels_in_grid(grid,snum)

cache={}
total = memget_subgrid_total_power(grid,33,45,3,cache)
new_total = memget_subgrid_total_power(grid,33,45,4,cache)

max_list = calc_all_subgrids(grid)
(max, max_grid_location, sqsize) = find_max_subgrid_from_allsubgrids(max_list)

print(max)
print(max_grid_location)
print(sqsize)




            

