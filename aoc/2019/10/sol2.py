import sys
import math

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
        if abs(self.x-other.x)<0.01 and abs(self.y-other.y)<0.01:
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
# printSpaceMap(spaceMap,allRocks)
#

def printSpaceMap(spaceMap,allRocks,ptOrigin,ptRemoved=''):

    # print header
    header = ' '
    for x in range(0,len(spaceMap[0])):
        header = header + '%i' % (x % 10) 
    print(header)

    for y in range(0,len(spaceMap)):
        rowContents = '%i' % (y % 10)
        row = spaceMap[y]
        for x in range(0,len(row)):
            ptTest = Point(x,y)
            if ptTest in allRocks:
                if ptTest == ptOrigin:
                    rowContents = rowContents + 'O'
                else:
                    rowContents = rowContents + '+'
            elif ptTest == ptRemoved:
                rowContents = rowContents + 'X'
            else:
                rowContents = rowContents + '.'
        print(rowContents)



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
                #print('rock at %i %i' % (x,y))
    print('number of rocks %i' % (len(allPoints)))
    return allPoints



#-------------------------------------------------------------
# getDistanceBtwnTwoRocks
#
# Given point A and point B,
#
#      B
#     /
#    /
#   A
# 
# H = hypotenuse = distance from A to B
# H = sqrt(dx^2+dy^2)
#

def getDistanceBtwnTwoRocks(ptStart,ptTarget):
    dx = round(ptTarget.x-ptStart.x,6)
    dy = round(-(ptTarget.y-ptStart.y),6)
    dist = math.sqrt(dx*dx+dy*dy)
    if dist<0.1:
        print('%i %i to %i %i' % (ptStart.x,ptStart.y,ptTarget.x,ptTarget.y))
    return (dx,dy,dist)


#-------------------------------------------------------------
# getAngleBtwnTwoRocks
#
#
# Given point A and point B,
# how to measure angle 
#
#      B
#     /
#    /
#   A
# 
# H = hypotenuse = distance from A to B
# H = sqrt(dx^2+dy^2)
# sin(angle) = dy/H
# angle = arcsin(dy/H)


def getAngleBtwnTwoRocks(ptStart,ptTarget):
    (dx,dy,dist) = getDistanceBtwnTwoRocks(ptStart,ptTarget)
   
    # let's get the 0, 90, 180, 270
    # up
    if dx==0.0 and dy<0.0:
        return 180

    # right, 90
    if dx>0.0 and dy==0.0:
        return 90

    # down 180
    if dx==0.0 and dy>0.0:
        return 0

    # left 270
    if dx<0.0 and dy==0.0:
        return 270

    if dx>0 and dy>0:
        value = dy/dist
        radian = math.asin(value)
        angle = round(radian*180/math.pi,6)
        angle = 90 - angle

    if dx>0 and dy<0:
        value = abs(dy/dist)
        radian = math.asin(value)
        angle = round(radian*180/math.pi,6)
        angle = angle + 90
    
    if dx<0 and dy<0:
        value = abs(dy/dist)
        radian = math.asin(value)
        angle = round(radian*180/math.pi,6)
        angle = 270 - angle

    if dx<0 and dy>0:
        value = abs(dy/dist)
        radian = math.asin(value)
        angle = round(radian*180/math.pi,6)
        angle = 270 + angle

    while (angle<0):
        angle = angle+360
    return angle


#-------------------------------------------------------
# getAngleBtwnRocksToOrigin
#
#

def getAngleBtwnRocksToOrigin(ptStart,allRocks):
    rockAngle = {}
    for rock in allRocks:
        #print('checking for rock %i %i' % (rock.x,rock.y))
        if rock==ptStart:
            continue
        angle = getAngleBtwnTwoRocks(ptStart,rock)
        if angle not in rockAngle:
            rockAngle[angle] = rock
            #print('(%i %i) %f' % (rock.x,rock.y,angle))
        else:
            # same angle as previous rock
            # now we see which rock is closer to origin
            # the rock closer to origin will get hit first
            prevRock = rockAngle[angle]
            curRock = rock
            (dx,dy,prevDist) = getDistanceBtwnTwoRocks(ptStart,prevRock)
            (dx,dy,curDist) = getDistanceBtwnTwoRocks(ptStart,curRock)
            if curDist < prevDist:
                rockAngle[angle] = curRock
                print('(%i %i) %f dist %f override (%i %i) dist %f' % 
                   (rock.x,rock.y,angle,curDist,prevRock.x,prevRock.y,prevDist))
    return rockAngle



#-------------------------------------------------------
# printRockAngles
# 

def printRockAngles(rockAngle):
    num = 1
    sortedAngles = sorted(rockAngle.keys())
    for a in sortedAngles:
        rock = rockAngle[a]
        print('%i %f (%i %i)' % (num,a,rock.x,rock.y))
        num = num+1


#-------------------------------------------------------
# shootRocks
#

def shootRocks(ptStart,spaceMap):
    allRocks = getAllRocks(spaceMap)

    num = 1 
    while len(allRocks)>1:
        rockAngle = getAngleBtwnRocksToOrigin(ptStart,allRocks)
        printRockAngles(rockAngle)

        # now remove all our hit rocks from first rotation
        # from main list of rocks
        for angle in sorted(rockAngle.keys()):
            r = rockAngle[angle]
            print('%i num rock removed at %i,%i  angle %f' % (num,r.x,r.y,angle))
            num = num+1
            allRocks.remove(r)
            printSpaceMap(spaceMap,allRocks,ptStart,r)
        print('num rocks remaining %i' % len(allRocks))


#-------------------------------------------------------
# tests
#
#   012345678
# 0 FE  D 
# 1 
# 2 G H J
# 3
# 4 C B A
#

pJ = Point(4,2)
pD = Point(4,0)
pF = Point(0,0)
pE = Point(1,0)
pH = Point(2,2)
pG = Point(0,2)
pC = Point(0,4)
pB = Point(2,4)
assert(round(getAngleBtwnTwoRocks(pH,pC),1)==225.0)
assert(round(getAngleBtwnTwoRocks(pJ,pC),1)==243.4)

assert(round(getAngleBtwnTwoRocks(pC,pH),1)==45.0)
assert(round(getAngleBtwnTwoRocks(pC,pJ),1)==63.4)

assert(round(getAngleBtwnTwoRocks(pD,pG),1)==243.4)
assert(round(getAngleBtwnTwoRocks(pJ,pF),1)==296.6)
assert(round(getAngleBtwnTwoRocks(pG,pD),1)==63.4)
assert(round(getAngleBtwnTwoRocks(pF,pJ),1)==116.6)

assert(round(getAngleBtwnTwoRocks(pH,pG),1)==270.0)
assert(round(getAngleBtwnTwoRocks(pG,pB),1)==135.0)
assert(round(getAngleBtwnTwoRocks(pC,pH),1)==45.0)
assert(round(getAngleBtwnTwoRocks(pG,pH),1)==90.0)
assert(round(getAngleBtwnTwoRocks(pG,pF),1)==0.0)
assert(round(getAngleBtwnTwoRocks(pG,pC),1)==180.0)

#input = getInput('test21.txt')
#spaceMap = convertTextToMap(input)
#print(spaceMap)
#ptStart = Point(8,3)
#shootRocks(ptStart,spaceMap)

#input = getInput('test5.txt')
#spaceMap = convertTextToMap(input)
#ptStart = Point(11,13)
#shootRocks(ptStart,spaceMap)

input = getInput('input.txt')
spaceMap = convertTextToMap(input)
ptStart = Point(26,28)
shootRocks(ptStart,spaceMap)

