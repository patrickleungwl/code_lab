# check triangles
#
# a valid triangle is where sum of any two sides > 3rd side
#

def is_triangle(side0, side1, side2):

    s0 = int(side0)
    s1 = int(side1)
    s2 = int(side2)
    if s0 + s1 > s2 and \
       s1 + s2 > s0 and \
       s2 + s0 > s1:
        return True

    return False



def check_triangles_in_col( col ):
    # now go thru each col
    num_triangles = 0
    for i in range(0,len(col),3):
        if is_triangle(col[i], col[i+1], col[i+2]):
            num_triangles += 1
    return num_triangles


def check_triangles():
    f = open('input.txt', 'r')
    col1 = []
    col2 = []
    col3 = []
    for line in f:
        line = line.rstrip()
        sides = line.split()
        col1.append(sides[0])
        col2.append(sides[1])
        col3.append(sides[2])

    triangles  = check_triangles_in_col(col1)
    triangles += check_triangles_in_col(col2)
    triangles += check_triangles_in_col(col3)

    print("Number of triangles %i" % triangles)


check_triangles()

