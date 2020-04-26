
# Declare class position to keep track of current position
# x,y       = coordinates
# dir       = 0:N, 1:E, 2:S, 3:W

class Position:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.cache = {}

    # expect a space-delimited series of commands
    def make_moves(self, commands):
        for c in commands.split():
            self.make_move(c)


    def make_move(self, command):
        turn_dir = command[0:1]
        num_paces_forward = int(command[1:])

        if turn_dir == 'R':
            self.dir = self.dir + 1
        if turn_dir == 'L':
            self.dir = self.dir - 1

        self.dir = self.dir % 4     # ensure 4->0, 5->1, etc

        # store the cells crossed

        for num in range(0,num_paces_forward):

            # now add the number of paces in the set direction
            # 0 = north
            if self.dir == 0:
                self.y = self.y + 1

            # 1 = east
            if self.dir == 1:
                self.x = self.x + 1

            # 2 = south
            if self.dir == 2:
                self.y = self.y - 1

            # 3 = west
            if self.dir == 3:
                self.x = self.x - 1

            pos = "%i_%i" % (self.x, self.y)
            if pos in self.cache:
                print("Found dup %s" % (pos))
                dist = self.get_distance_to_origin()
                print("Distance to origin %s" % (dist))

            self.cache[pos] = pos


    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_distance_to_origin(self):
        distance = 0 
        distance = abs(self.x)
        distance = distance + abs(self.y)
        return distance


# Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
# R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
# R5, L5, R5, R3 leaves you 12 blocks away.

# R2 L3, using x,y coords
#   - Right
#   - Forward 2,  (2,0)
#   - Left
#   - Forward 3   (2,3)
#   = (2,3)
#
# current_pos_x, y = x,y coordinate
# current_dir      = 0:N, 1:E, 2:S, 3:W

def test():
    #p = Position(0,0,0)
    #p.make_move("R3")
    #print("Distance should be 3, %s" % (p.get_distance_to_origin()) )
    #p.make_move("L1")
    #print("Distance should be 4, %s" % (p.get_distance_to_origin()) )

    #p2 = Position(0,0,0)
    #p2.make_moves("R3 L1")
    #print("Distance should be 4, %s" % (p2.get_distance_to_origin()) )

    p3 = Position(0,0,0)
    p3.make_moves("R1 L4 L5 L5 R2 R2 L1 L1 R2 L3 R4 R3 R2 L4 L2 R5 L1 R5 L5 L2 L3 L1 R1 R4 R5 L3 R2 L4 L5 R1 R2 L3 R3 L3 L1 L2 R5 R4 R5 L5 R1 L190 L3 L3 R3 R4 R47 L3 R5 R79 R5 R3 R1 L4 L3 L2 R194 L2 R1 L2 L2 R4 L5 L5 R1 R1 L1 L3 L2 R5 L3 L3 R4 R1 R5 L4 R3 R1 L1 L2 R4 R1 L2 R4 R4 L5 R3 L5 L3 R1 R1 L3 L1 L1 L3 L4 L1 L2 R1 L5 L3 R2 L5 L3 R5 R3 L4 L2 R2 R4 R4 L4 R5 L1 L3 R3 R4 R4 L5 R4 R2 L3 R4 R2 R1 R2 L4 L2 R2 L5 L5 L3 R5 L5 L1 R4 L1 R1 L1 R4 L5 L3 R4 R1 L3 R4 R1 L3 L1 R1 R2 L4 L2 R1 L5 L4 L5")
    print("Distance is %s" % (p3.get_distance_to_origin()) )

test()

