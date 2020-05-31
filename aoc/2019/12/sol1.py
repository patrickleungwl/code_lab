import sys

class Moon:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

        self.vx = 0
        self.vy = 0
        self.vz = 0

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
            if self.x-other.x==0 and self.y-other.y==0:
                return True
            else:
                return False

    def getEnergy(self):
        pot = abs(self.x) + abs(self.y) + abs(self.z)
        kin = abs(self.vx) + abs(self.vy) + abs(self.vz)
        energy = pot * kin
        return energy



def simulate(moons,numSteps):

    # apply gravity
    for r in range(0,numSteps):
        for m in moons:
            for mo in moons:
                if m == mo:
                    continue

                m.updateVelocity(mo)

        te = 0
        print('step %i' % int(r+1))
        for m in moons:
            m.updatePosition()
            m.print2()
            te = te + m.getEnergy()

        print('energy = %i' % te)
        print('')





moons = []
moons.append(Moon(-1,0,2))
moons.append(Moon(2,-10,-7))
moons.append(Moon(4,-8,8))
moons.append(Moon(3,5,-1))
simulate(moons,10)

#moons2 = []
#moons2.append(Moon(-8,-10,0))
#moons2.append(Moon(5,5,10))
#moons2.append(Moon(2,-7,3))
#moons2.append(Moon(9,-8,-3))
#simulate(moons2,100)
#
#moons3 = []
#moons3.append(Moon(17,-12,13))
#moons3.append(Moon(2,1,1))
#moons3.append(Moon(-1,-17,7))
#moons3.append(Moon(12,-14,18))
#simulate(moons3,1000)

