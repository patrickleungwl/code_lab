import sys

# Point
#  wrapper class around coordinates x,y
#

class Point:
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)
        self.hasAsteroid = False

    # is this other instance equivalent to 
    # this current one?
    def __eq__(self,other):
        if abs(self.x-other.x)<0.0001 and abs(self.y-other.y)<0.0001:
            return True
        else:
            return False

    def setAsteroid(self):
        self.hasAsteroid = True 

    def hasAsteroid(self):
        print('hasAsteroid %i %i' % (self.x,self.y))
        return self.hasAsteroid

    def toIntxy(self):
        xint = int(self.x)
        yint = int(self.y)
        if abs(self.x - xint) < 0.0001 and abs(self.y - yint) < 0.0001:
            return (True, xint, yint)
        else:
            return (False, 0, 0)


def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp



def convert_text_to_map(input):
    rows = input.split('\n')
    space_map = [] # rows
    for r in rows:
        space_row = []
        if len(r)==0:
            break
        for i in range(0,len(r)):
            if r[i] == '#':
                space_row.append(1)
            else:
                space_row.append(0)
        space_map.append(space_row)
    return space_map


# is_vertical

def is_vertical(srcPt, tgtPt):
    if abs(tgtPt.x - srcPt.x) < 0.1:
        return True
    return False


# get_slope
#  find the slope- dy/dx between 
#  points source (xs,ys) 
#  and    target (xt,yt) 

def get_slope(srcPt, tgtPt):
    dx = float(tgtPt.x -srcPt.x)
    dy = tgtPt.y - srcPt.y 
    m  = dy / dx
    return m

# get_path
#  return the set of points in between
#  srcPt and tgtPt

def get_path(srcPt, tgtPt):
    points = []
    isReversed = False

    if is_vertical(srcPt, tgtPt):
        start_y = srcPt.y
        target_y = tgtPt.y  
        if target_y < start_y:
            start_y = tgtPt.y
            target_y = srcPt.y
            isReversed = True
        y = start_y + 1.0
        while y <= target_y:
            pt = Point(srcPt.x,y)
            points.append(pt)
            y = y + 1.0
    else:
        # this is a slope

        m = get_slope(srcPt, tgtPt)
        print('slope m %f' % m)

        dx = 1.0
        start_x = srcPt.x
        target_x = tgtPt.x
        if target_x < start_x:
            start_x = tgtPt.x
            target_x = srcPt.x
            isReversed = True
            dx = -1.0
        # should we go left?


        x = start_x + dx
        while x <= target_x:
            y = srcPt.y + (m*x)
            pt = Point(x,y)
            points.append(pt)
            x = x + 1.0

    if isReversed:
        points.reverse()

    return points


def get_all_map_points(space_map):
    allPoints = []
    for y in range(0,len(space_map)):
        row = space_map[y]
        for x in range(0,len(row)):
            p = Point(x,y)
            if space_map[y][x] == 1:
                p.setAsteroid()
            allPoints.append(p)
    return allPoints



# now for every point in map
# for each point A
#   to each target point B
#       is there an asteroid at B?
#           calc the path from A to B
#           are there any asteroids along its path?
#           if yes, then A to B is blocked
#           

def generate_space_view_map(spaceMap):
    allPoints = get_all_map_points(spaceMap)
    for srcP in allPoints:
        if not srcP.hasAsteroid:
            continue

        print('checking asteroid at- %i %i' % (srcP.x,srcP.y))

        # now let's scan all other asteroids from x,y
        totalAsteroidCanView = 0
        targetPoints = get_all_map_points(spaceMap)
        for tgtP in targetPoints:
            if not tgtP.hasAsteroid:
                continue

            if srcP == tgtP:
                continue

            print('  checking src (%f %f) to (%f %f)' % (srcP.x, srcP.y, tgtP.x, tgtP.y))
            
            # once we have all the points along the path
            # check- 
            #  does the point contain an asteroid
            #  is the asteroid the target?  
            #    if yes, then can view
            #    if not, then view is blocked
            canView = False
            pathPoints = get_path(srcP,tgtP)
            for p in pathPoints:
                print('    path %f %f' % (p.x,p.y))
                if p == tgtP:
                    print(' canview %f %f' % (p.x,p.y))
                    canView = True
                    break
            
            if canView:
                totalAsteroidCanView = totalAsteroidCanView+1

        print('  totalAsteroidCanView %f' % totalAsteroidCanView)


ptOrigin = Point(1,0)
ptTargetA = Point(0,2)
pathPoints = get_path(ptOrigin, ptTargetA)
p = pathPoints[0]
print('%i' % len(pathPoints))
print('test %f %f' % (p.x, p.y))


ptOrigin = Point(0,0)
ptTargetA = Point(4,4)
ptTargetB = Point(4,2)
ptTargetC = Point(4,0)
ptTargetD = Point(0,4)
ptTargetE = Point(1,0)
assert(get_slope(ptOrigin, ptTargetA)==1.0)
assert(get_slope(ptOrigin, ptTargetB)==0.5)

# 45 degree path
pathPoints = get_path(ptOrigin, ptTargetA)
assert(len(pathPoints)==4)
assert(Point(1,1) == pathPoints[0])
assert(Point(2,2) == pathPoints[1])
assert(Point(3,3) == pathPoints[2])
assert(Point(4,4) == pathPoints[3])

## 22.5 degree path
pathPoints = get_path(ptOrigin, ptTargetB)
assert(len(pathPoints)==4)
assert(Point(1,0.5) == pathPoints[0])
assert(Point(2,1) == pathPoints[1])
assert(Point(3,1.5) == pathPoints[2])
assert(Point(4,2) == pathPoints[3])

# horizonal right path
pathPoints = get_path(ptOrigin, ptTargetC)
assert(len(pathPoints)==4)
assert(Point(1,0) == pathPoints[0])
assert(Point(2,0) == pathPoints[1])
assert(Point(3,0) == pathPoints[2])
assert(Point(4,0) == pathPoints[3])

# horizonal left path
pathPoints = get_path(ptTargetC, ptOrigin)
assert(len(pathPoints)==4)
assert(Point(4,0) == pathPoints[0])
assert(Point(3,0) == pathPoints[1])
assert(Point(2,0) == pathPoints[2])
assert(Point(1,0) == pathPoints[3])

# vertical down path
pathPoints = get_path(ptOrigin, ptTargetD)
assert(len(pathPoints)==4)
assert(Point(0,1) == pathPoints[0])
assert(Point(0,2) == pathPoints[1])
assert(Point(0,3) == pathPoints[2])
assert(Point(0,4) == pathPoints[3])

# vertical up path
pathPoints = get_path(ptTargetD, ptOrigin)
assert(len(pathPoints)==4)
assert(Point(0,4) == pathPoints[0])
assert(Point(0,3) == pathPoints[1])
assert(Point(0,2) == pathPoints[2])
assert(Point(0,1) == pathPoints[3])

# next point over
pathPoints = get_path(ptOrigin, ptTargetE)
assert(len(pathPoints)==1)
assert(Point(1,0) in pathPoints)

map1 = get_input('test1.txt')
spaceMap = convert_text_to_map(map1)
# y=0, x=1
assert(spaceMap[0][1] == 1)
generate_space_view_map(spaceMap)



