import math
import collections

# ThreeD
# Wrap 3 dimensional data into one data structure

class ThreeD:
    x = 0
    y = 0
    z = 0

    def __init__(self, tx, ty, tz):
        self.x = tx
        self.y = ty
        self.z = tz

    # override comparison operator to compare by value
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

    def __hash__(self):
        return self.x *100 + self.y * 10 + self.z


    
# Particle
# Let each particle figure things out for itself

class Particle:

    pos = None
    vel = None
    acl = None
    id = 0

    def __init__(self, tid, tpos, tvel, tacl):
        self.id = tid
        self.pos = tpos
        self.vel = tvel
        self.acl = tacl

    def move(self):
        self.vel.x = self.vel.x + self.acl.x
        self.vel.y = self.vel.y + self.acl.y
        self.vel.z = self.vel.z + self.acl.z

        self.pos.x = self.pos.x + self.vel.x
        self.pos.y = self.pos.y + self.vel.y
        self.pos.z = self.pos.z + self.vel.z

        distance_to_center = self.get_distance_to_center()
        #print('%s p=%s,%s,%s v=%s,%s,%s a=%s,%s,%s  d=%s' 
        #        % (self.id, 
        #           self.pos.x, self.pos.y, self.pos.z, 
        #           self.vel.x, self.vel.y, self.vel.z, 
        #           self.acl.x, self.acl.y, self.acl.z,
        #           distance_to_center))

    def get_distance_to_center(self):
        # s = sqrt(x^2+y^2+z^2)
        xs = math.pow(self.pos.x,2)
        ys = math.pow(self.pos.y,2)
        zs = math.pow(self.pos.z,2)
        s = math.sqrt(xs+ys+zs)
        return s


# parse_str_into_vector
# Convert string into a ThreeD data structure 

def parse_str_into_vector(attribute):
    attribute = attribute.replace('>','')
    idx = attribute.find('<')+1
    core_attribute = attribute[idx:]
    corea = core_attribute.split(',')
    vector = ThreeD(int(corea[0]),int(corea[1]),int(corea[2])) 
    return vector


# read_input
# Gets a list of Particles from input file 

def read_input(input_file):
    particles = []
    with open('data.txt', 'r') as file:
        idx = 0
        data = file.read()
        rows = data.split('\n')
        for row in rows:
            if len(row)<1:
                break
            print(row)
            attributes = row.split('>,')
            pos = parse_str_into_vector(attributes[0])
            vel = parse_str_into_vector(attributes[1])
            acl = parse_str_into_vector(attributes[2])
            p = Particle(idx,pos,vel,acl)
            idx = idx+1
            particles.append(p)
    return particles


def simulate_motion(particles):
    for i in range(0,10000):
        print('*** Move %s ****' % i)
        positions = {}
        collided_particles = set()
        for pidx in range(0,len(particles)):
            p = particles[pidx]
            p.move()
            if p.pos in positions:
                pother = positions[p.pos]
                collided_particles.add(pidx)
                collided_particles.add(pother)
                print('idx %s and %s collided' % (pidx, pother))        
            else:
                positions[p.pos] = pidx
                    
        # now remove the collided particles- in reverse order
        collided = sorted(collided_particles)
        for cidx in reversed(collided):
            del particles[cidx]
    print('Number of particles left = %s' % len(particles))


input_name = 'data.txt'
particles = read_input(input_name)
simulate_motion(particles)

#pos = ThreeD(3,4,5)
#vel = ThreeD(1,2,3)
#acl = ThreeD(1,1,1)
#p = Particle(1, pos, vel, acl)
#p.move()
#print(p.get_distance_to_center())

#pos1 = ThreeD(3,4,5)
#pos2 = ThreeD(3,4,5)
#print(pos1==pos2)
#p = []
#p.append(pos1)
#print(pos2 in p)  # true! 

#pdict = {}
#pdict[pos1] = pos1 
#print(pos1 in pdict)
#print(pos2 in pdict)
#val = pdict[pos2]
#print(val.y)


#pos1 = ThreeD(3,4,5)
#pos2 = ThreeD(1,2,3)
#pos3 = ThreeD(1,1,1)
#pos4 = ThreeD(1,2,3)
#pos5 = ThreeD(1,8,3)

#p = []
#p.append(pos1)
#p.append(pos2)
#p.append(pos3)
#p.append(pos4)
#p.append(pos5)
#
#s = set()
#s.add(3)
#s.add(1)
#s.add(1)
#print(s)
#mylist = sorted(s)
#print(mylist)
#for r in reversed(mylist):
####    print(r)
