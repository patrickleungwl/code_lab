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

    def isAt(self,other):
        if abs(self.x-other.x)<0.002 and abs(self.y-other.y)<0.002:
            return True
        else:
            return False

    def isNear(self,other):
        if abs(self.x-other.x)<2.0 and abs(self.y-other.y)<2.0:
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


#-------------------------------------------------------------
# getInput
# 

def getInput(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


#-------------------------------------------------------------
# convertTextToMap
#

def convertTextToMap(input):
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


#-------------------------------------------------------------
# getIncrementalDxDy
#

def getIncrementalDxDy(ptStart,ptEnd):
    dx = (ptEnd.x - ptStart.x) / 10000.0
    dy = (ptEnd.y - ptStart.y) / 10000.0
    return (dx,dy)


#-------------------------------------------------------------
# getApproximateDxDy
#

def getApproximateDxDy(ptStart,ptEnd):
    dx = (ptEnd.x - ptStart.x) / 1000.0
    dy = (ptEnd.y - ptStart.y) / 1000.0
    return (dx,dy)


#-------------------------------------------------------------
# getAllRocks
#

def getAllRocks(space_map):
    allPoints = []
    for y in range(0,len(space_map)):
        row = space_map[y]
        for x in range(0,len(row)):
            if space_map[y][x] == 1:
                p = Point(x,y)
                p.setAsteroid()
                allPoints.append(p)
    return allPoints



#-------------------------------------------------------------
# generateSpaceViewMap
#
# now for every point in map
# for each point A
#   to each target point B
#       is there an asteroid at B?
#           calc the path from A to B
#           are there any asteroids along its path?
#           if yes, then A to B is blocked
#           

def generateSpaceViewMap(spaceMap):
    allRocks = getAllRocks(spaceMap)
    maxRockViewCount = 0
    for srcP in allRocks:

        # now let's scan all other asteroids from x,y
        totalRockViewCount = 0
        otherRocks = getAllRocks(spaceMap)
        for otherP in otherRocks:
            if srcP == otherP:
                continue
           
            # now let's see if any rocks are in btween srcP to otherP
            blocked = False
            allRocks = getAllRocks(spaceMap)
            for oneP in allRocks:
                if isBlocked(srcP,otherP,oneP):
                    blocked = True
                    break
            
            if blocked == False:
                totalRockViewCount = totalRockViewCount+1
            canSee = not blocked
            #print('  (%f %f) to (%f %f) = canSee %s' % (srcP.x, srcP.y, otherP.x, otherP.y, canSee))

        if totalRockViewCount > maxRockViewCount:
            maxRockViewCount = totalRockViewCount
            print('  maxView %f at (%f %f)' % (maxRockViewCount, srcP.x, srcP.y))

#-------------------------------------------------------------
# isOutsideStartAndEndBorders
#
# we try to optimise a bit and check if the rock under test
# is without our starting rock and ending rock region
#
# if the test rock is outside our starting and ending rock region
# then should just return True
# and we can avoid testing this rock since we already know
# that it's outside our region and so cannot get in the way 
# of viewing between starting rock and ending rock points
#

def isOutsideStartAndEndBorders(ptStart,ptEnd,ptTest):
    # let's optimise a bit
    # we can assume there is no block if
    #   ptTest.x is not in between ptStart.x and ptEnd.x
    # OR
    #   ptTest.y is not in between ptStart.y and ptEnd.y 

    # leftX is smaller than rightX
    leftX = ptStart.x
    rightX = ptEnd.x
    if leftX > rightX:
        leftX = ptEnd.x
        rightX = ptStart.x

    # topY is smaller than bottomY
    topY = ptStart.y
    bottomY = ptEnd.y
    if topY > bottomY:
        topY = ptEnd.y
        bottomY = ptStart.y

    if ptTest.x < leftX or ptTest.x > rightX:
        return True
    if ptTest.y < topY or ptTest.y > bottomY:
        return True

    return False


#-------------------------------------------------------------
# isBlocked
#
# check if ptTest is between line with endpoints ptStart and ptEnd
# 

def isBlocked(ptStart,ptEnd,ptTest,debug=False):
    if debug:
        print(' isBlocked start(%f %f) end(%f %f) test(%f %f)' %
                (ptStart.x, ptStart.y, ptEnd.x, ptEnd.y, ptTest.x, ptTest.y))
    if ptStart.isAt(ptTest):
        return False
    if isOutsideStartAndEndBorders(ptStart,ptEnd,ptTest):
        return False

    (idx,idy) = getIncrementalDxDy(ptStart,ptEnd)
    (adx,ady) = getApproximateDxDy(ptStart,ptEnd)
    dx = idx
    dy = idy
    while (not ptStart.isAt(ptEnd)):
        # we've hit our test, so there is a block
        if ptStart.isAt(ptTest):
            return True

        newX = ptStart.x + dx
        newY = ptStart.y + dy
        ptStart = Point(newX,newY)
        if debug:
            print(' checking %f %f' % (newX, newY))

    # we've hit our target, so there is no block
    if ptStart.isAt(ptEnd):
        return False

    # by default there is a block
    return True


#   012345678
# 0 FE  D 
# 1 
# 2 G H
# 3
# 4 C B A
#
#
# F cannot see D because E is in the way.
# F cannot see A because H is in the way.
# F cannot see C because G is in the way.
# A cannot see F because H is in the way.
# C cannot see F because G is in the way.
# A cannot see C because B is in the way.
# C cannot see A because B is in the way.

pF = Point(0,0)
pE = Point(1,0)
pD = Point(4,0)
pG = Point(0,2)
pC = Point(0,4)
pH = Point(2,2)
pA = Point(4,4)
pB = Point(2,4)

assert(isBlocked(pF,pC,pG))
assert(isBlocked(pC,pF,pG))
assert(isBlocked(pF,pD,pE))
assert(isBlocked(pF,pE,pE)==False)
assert(isBlocked(pE,pF,pF)==False)
assert(isBlocked(pE,pF,pF)==False)

assert(isBlocked(pG,pD,pD)==False)
assert(isBlocked(pD,pG,pG)==False)
assert(isBlocked(pF,pG,pG)==False)
assert(isBlocked(pF,pH,pH)==False)
assert(isBlocked(pF,pA,pH))
assert(isBlocked(pA,pF,pH))
assert(isBlocked(pA,pH,pH)==False)

assert(isBlocked(pD,pB,pH)==False)
assert(isBlocked(pB,pD,pH)==False)
assert(isBlocked(pB,pE,pH)==False)
assert(isBlocked(pE,pB,pH)==False)

assert(isBlocked(pC,pD,pH))
assert(isBlocked(pD,pC,pH))
assert(isBlocked(pD,pH,pH)==False)
assert(isBlocked(pC,pH,pH)==False)
assert(isBlocked(pH,pC,pC)==False)

pS = Point(4,2)
pE = Point(1,2)
pT0 = Point(0,2)
pT1 = Point(1,2)
pT2 = Point(2,2)
pT3 = Point(3,2)
assert(isBlocked(pS,pE,pT0)==False)
assert(isBlocked(pS,pE,pT1)==False)
assert(isBlocked(pS,pE,pT2))
assert(isBlocked(pS,pE,pT3))

infile = getInput('input.txt')
spaceMap = convertTextToMap(infile)
print(spaceMap)
generateSpaceViewMap(spaceMap)

infile = getInput('test1.txt')
spaceMap = convertTextToMap(infile)
print(spaceMap)
generateSpaceViewMap(spaceMap)

infile = getInput('test2.txt')
spaceMap = convertTextToMap(infile)
print(spaceMap)
generateSpaceViewMap(spaceMap)

infile = getInput('test3.txt')
spaceMap = convertTextToMap(infile)
print(spaceMap)
generateSpaceViewMap(spaceMap)

infile = getInput('test4.txt')
spaceMap = convertTextToMap(infile)
print(spaceMap)
generateSpaceViewMap(spaceMap)

infile = getInput('test5.txt')
spaceMap = convertTextToMap(infile)
print(spaceMap)
generateSpaceViewMap(spaceMap)


