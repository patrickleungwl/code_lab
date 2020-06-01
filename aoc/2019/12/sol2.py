import sys
import hashlib


class Moon:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

        self.vx = 0
        self.vy = 0
        self.vz = 0


    def getState(self,axis):
        if axis==-1:
            stateMark = '%i%i%i%i%i%i' % (self.x, self.vx, \
                self.y, self.vy, self.z, self.vz)
        if axis==0:
            stateMark = '%i%i' % (self.x, self.vx)
        if axis==1:
            stateMark = '%i%i' % (self.y, self.vy)
        if axis==2:
            stateMark = '%i%i' % (self.z, self.vz)
        return stateMark


    def print2(self):
        e = self.getEnergy()
        print('p:%3i %3i %3i  v:%3i %3i %3i  e:%3i' 
                % (self.x, self.y, self.z, self.vx, self.vy, self.vz, e))


    def updatePosition(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.z = self.z + self.vz


    def updateVelocity(self,other):
        if other.x > self.x:
            self.vx = self.vx + 1
        if other.x < self.x:
            self.vx = self.vx - 1

        if other.y > self.y:
            self.vy = self.vy + 1
        if other.y < self.y:
            self.vy = self.vy - 1

        if other.z > self.z:
            self.vz = self.vz + 1
        if other.z < self.z:
            self.vz = self.vz - 1

    # is this other instance equivalent to 
    # this current one?
        def __eq__(self,other):
            if self.x==other.x and self.y==other.y:
                return True
            else:
                return False


    def getEnergy(self):
        pot = abs(self.x) + abs(self.y) + abs(self.z)
        kin = abs(self.vx) + abs(self.vy) + abs(self.vz)
        energy = pot * kin
        return energy

def findCommonMultiple(r1,r2,r3):

    t1 = r1
    t2 = r2
    t3 = r3
    nn=0
    num=0
    while True:
        if t1 < t2 or t1 < t3:
            t1 = t1 + r1
        if t2 < t1 or t2 < t3:
            t2 = t2 + r2
        if t3 < t1 or t3 < t1:
            t3 = t3 + r3
        if t1 == t2 and t2 == t3:
            break
        num = num+1
        if num % 100000000 == 0:
            num = 0
            nn = nn+1
            print('%i' % nn)
    print('%i %i %i' % (t1,t2,t3))



def getHashedStateOfAllMoons(moons,axis):

    totalState = ''
    for m in moons:
        state = m.getState(axis)
        totalState = totalState + state

    totalState = totalState.encode('utf-8')
    hash = int(hashlib.sha1(totalState).hexdigest(),16)

    return hash


def simulate(moons,axis):

    print('simulate axis=%i' % axis)

    # apply gravity
    numStep = 0
    states = {}

    startState = getHashedStateOfAllMoons(moons,axis)
    states[startState] = 0

    while True:
        for m in moons:
            for mo in moons:
                if m == mo:
                    continue

                m.updateVelocity(mo)

        #print('step %i' % int(numStep+1))

        for m in moons:
            m.updatePosition()
            #m.print2()

        hash = getHashedStateOfAllMoons(moons,axis)
        if hash in states:
            prevStep = states[hash]
            print('%i state appeared in step %i' % (numStep+1,prevStep))
            return (numStep+1)
        else:
            states[hash] = numStep 

        numStep = numStep + 1
        if numStep % 1000000 == 0:
            print(numStep)


#moons = []
#moons.append(Moon(-1,0,2))
#moons.append(Moon(2,-10,-7))
#moons.append(Moon(4,-8,8))
#moons.append(Moon(3,5,-1))
#testmoons = moons
#r0 = simulate(testmoons,-1)
#
#testmoons = moons
#r1 = simulate(testmoons,0)
#testmoons = moons
#r2 = simulate(testmoons,1)
#testmoons = moons
#r3= simulate(testmoons,2)
#
#findCommonMultiple(r1,r2,r3)

moons2 = []
moons2.append(Moon(-8,-10,0))
moons2.append(Moon(5,5,10))
moons2.append(Moon(2,-7,3))
moons2.append(Moon(9,-8,-3))

testmoons = moons2
r1 = simulate(testmoons,0)
testmoons = moons2
r2 = simulate(testmoons,1)
testmoons = moons2
r3= simulate(testmoons,2)

findCommonMultiple(r1,r2,r3)


moons3 = []
moons3.append(Moon(17,-12,13))
moons3.append(Moon(2,1,1))
moons3.append(Moon(-1,-17,7))
moons3.append(Moon(12,-14,18))

testmoons = moons3
r1 = simulate(testmoons,0)
testmoons = moons3
r2 = simulate(testmoons,1)
testmoons = moons3
r3= simulate(testmoons,2)

findCommonMultiple(r1,r2,r3)


