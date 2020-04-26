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
    

def get_subgrid_total_power(grid,x,y):
    total = 0
    for tx in range(x,x+3):
        #print('**** %s' % (tx))
        for ty in range(y,y+3):
            #print('%s %s' % (tx,ty))
            total = total + grid[tx,ty]
    return total


def find_max_subgrid(grid):
    max = -100    
    max_grid_location = (0,0)
    for x in range(0,grid.shape[0]-3):
        for y in range(0,grid.shape[1]-3):
            total = get_subgrid_total_power(grid,x,y)
            if total > max:
                max = total
                max_grid_location = (x,y)
    return (max, max_grid_location)


assert calc_power_level(122,79,57)==-5, 'Power level test 1'
assert calc_power_level(217,196,39)==0, 'Power level test 2'
assert calc_power_level(101,153,71)==4, 'Power level test 3'

snum = 3613
grid = np.zeros((300,300))
set_power_levels_in_grid(grid,snum)
(max, max_grid_location) = find_max_subgrid(grid)
print(max)
print(max_grid_location)

#print(calc_power_level(33,46,18))
#print(calc_power_level(34,45,18))
#print(calc_power_level(35,45,18))
#print(calc_power_level(34,46,18))
#print(get_subgrid_total_power(grid,33,45))




            

