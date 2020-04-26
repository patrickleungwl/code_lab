# check triangles
#
# a valid triangle is where sum of any two sides > 3rd side
#

def is_triangle(sides):

    s0 = int(sides[0])
    s1 = int(sides[1])
    s2 = int(sides[2])
    if s0 + s1 > s2 and \
       s1 + s2 > s0 and \
       s2 + s0 > s1:
        return True

    return False



def check_triangles():
    f = open('input.txt', 'r')
    num_triangles = 0
    for line in f:
        line = line.rstrip()
        sides = line.split()
        if len(sides)!=3:
            print("not 3 sides %s" % sides )
            continue
        
        if is_triangle(sides):
            num_triangles += 1

    print("Number of triangles %i" % num_triangles)


check_triangles()

