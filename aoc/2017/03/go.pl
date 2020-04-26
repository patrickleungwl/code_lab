import math

def get_bottom_right_number(width):
    num = (width+width)+1
    num = num * num
    return num

def get_upper_left_number(width):
    num = width+width
    num = num * num
    num = num + 1
    return num

def get_bottom_left_number(width):
    br = get_bottom_right_number(width)
    ul = get_upper_left_number(width)
    diff = int((br - ul) / 2)
    bl = ul + diff
    return bl

def get_upper_right_number(width):
    br = get_bottom_right_number(width)
    ul = get_upper_left_number(width)
    diff = int((br - ul) / 2)
    ur = ul - diff
    return ur
 

def get_cube_corner_numbers(cubesize):
    br = get_bottom_right_number(cubesize)
    ul = get_upper_left_number(cubesize)
    bl = get_bottom_left_number(cubesize)
    ur = get_upper_right_number(cubesize)
    return (ur, ul, bl, br)


def get_xy_from_center_of_target_number(target):
    print(target)
    cubesize = 0

    while (get_bottom_right_number(cubesize)<target):
        cubesize = cubesize+1
    (ur, ul, bl, br) = get_cube_corner_numbers(cubesize)
    # which leg is target size in?
    midnum = 0
    if ur>target:
       midnum = ur-cubesize
       return (cubesize, target-midnum) 
    if ul>target:
        midnum = ul-cubesize
        return (midnum-target, cubesize)
    if bl>target:
        midnum = bl-cubesize
        return (-cubesize, midnum-target)
     
    midnum = br-cubesize
    return (target-midnum, -cubesize)
    
def get_distance_to_center(target):
    (cx, cy) = get_xy_from_center_of_target_number(target)
    distance = math.fabs(cx) + math.fabs(cy)
    return int(distance)


print(get_distance_to_center(1))
print(get_distance_to_center(12))
print(get_distance_to_center(23))
print(get_distance_to_center(1024))
print(get_distance_to_center(289326))







