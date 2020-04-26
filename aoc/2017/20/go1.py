import math

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
        min_particle = -1
        min_distance = 1000000000
        for pidx in range(0,len(particles)):
            p = particles[pidx]
            p.move()
            distance = p.get_distance_to_center()
            if distance < min_distance:
                min_particle = pidx
                min_distance = distance
        print('min particle %s at %s' % (min_particle, min_distance))


input_name = 'data.txt'
particles = read_input(input_name)
simulate_motion(particles)

#pos = ThreeD(3,4,5)
#vel = ThreeD(1,2,3)
#acl = ThreeD(1,1,1)
#p = Particle(1, pos, vel, acl)
#p.move()
#print(p.get_distance_to_center())


