import unittest

# Declare class position to keep track of current position

class Position:
    def __init__(self, pos):
        self.pos = pos

    # expect a space-delimited series of commands
    def make_moves(self, commands):
        for c in commands:
            self.make_move(c)


    def make_move(self, command):

        #     1
        #   2 3 4
        # 5 6 7 8 9
        #   A B C
        #     D
        # 
        # A=10 B=11 C=12 D=13
        #
        # must handle UDLR
        # U = up, pos-3
        # D = down, pos+3
        # L = left, pos-1
        # R = right, pos+1

        if command == 'U':
            if self.pos == 3 or self.pos == 13:
                self.pos -= 2
            elif self.pos > 5 and self.pos != 9:
                self.pos -= 4
        if command == 'D':
            if self.pos == 1 or self.pos == 11:
                self.pos += 2
            elif self.pos < 9 and self.pos != 5:
                self.pos += 4
        if command == 'L':
            if self.pos == 1 or self.pos == 2 or self.pos == 5 or self.pos == 10 or self.pos == 13:
                self.pos = self.pos
            else:
                self.pos -= 1
        if command == 'R':
            if self.pos == 1 or self.pos == 4 or self.pos == 9 or self.pos == 12 or self.pos == 13:
                self.pos = self.pos
            else:
                self.pos += 1


    def get_position(self):
        return self.pos



# Starting from the middle of a phone keypad- 5, 
#
# 1 2 3
# 4 5 6
# 7 8 9
#
# accept inputs consisting of UDLR- up down left right
# One line of input represents one code.
# The second and subsequent lines start from the end of the previous line.
# If a move is not possible, ignore it.

# current_pos = number

class TestPosition(unittest.TestCase):

    def setUp(self):
        self.p = Position(5)


    def test_basic_moves(self):
        self.p.make_move("L")
        self.assertEqual(self.p.get_position(), 5)

        # cannot go left beyond 4
        self.p.make_move("R")
        self.assertEqual(self.p.get_position(), 6)

        # go down
        self.p.make_move("D")
        self.assertEqual(self.p.get_position(), 10)

        # cannot go down beyond 10
        self.p.make_move("D")
        self.assertEqual(self.p.get_position(), 10)

        # go right right right right
        self.p.make_moves("RRRR")
        self.assertEqual(self.p.get_position(), 12)

        # go up up up 
        self.p.make_moves("UUUU")
        self.assertEqual(self.p.get_position(), 4)


#if __name__ == '__main__':
#    unittest.main()

#print("Position = %i" % 11 )
#print("Position = %i" % 13 )

p = Position(5)
p.make_moves("LUULRUULULLUDUDULDLUDDDLRURUDLRRDRDULRDDULLLRULLLURDDLRDLUUDDRURDDRDDDDRDULULLLLURDDLLRLUUDDDRLRRRDURLDDLRRLDUDRRRDLDLRRDLDLUURRLRULLULRUDRDLRUURLDRDLRLDULLLUDRDDRLURLUUDRLLLDRUUULLUULRUDDUDRDUURRRUDRLDDUURDUURUDRDDLULDDUDUDRRDDULUDULRDRULRLRLURURDULRUULLRDDDDRRUUDDDUUDRLLRUDRLRDLRRLULRLULRUDDULRLLLURLDDRLDDLRRLDRDDDRRLRUDRULUUDUURLDLRRULUDRDULDLLRRURRDDLRRRLULUDUUDDUDDLRDLRDRLRLDUDUDDUDLURRUURDRLRURLURRRLRLRRUDDUDDLUDRLUURUUDUUDDULRRLUUUDRLRLLUR")
print("Position = %i" % p.get_position() )
p.make_moves("LDLLRRLDULDDRDDLULRRRDDUDUDRRLLRUUULRUDLLRRDDRRLDDURUUDLUDRRLDURDDRUDLUDUUDLDLLLDLLLDRLLDLRUULULLUUDULDUUULDDLRUDLLUDLUUULDRLUDRULUUDLDURDLDUULLRDUDRDLURULDLUUUDURLDDRLLDRLRDDDUDRUULLDLUDRRDDLDLUURUDDLDRURRLULUDDURLDRDRDUDDRRULRLDURULULRURDUURRUDRDDRDRLDRDUUDLRULRDDDULRURUDRUUULUUDDLRRDDDUDRLRUDRDLRRUDLUDRULDDUDLRLDDLDRLRDLULRDRULRLLRLUDUURULLLDDUULUUDDDUDRRULDDDULRUDRRLRLLLUDLULDUUULDDULDUUDLUULRDLDUDRUDLLDLDLLULDDDDLUDDUDRUDLRRRDDDDDLLRRDRUUDDDRRULRUDUUDRULLDLLLDDRDDUURLUUURUDRUDURLRUUUULUUURDRRRULDUULDLDDDRDDDDLLDRUDRDURLDDURDURULDDRLLRRLDUDRDURRLDRDLLULUUUD")
print("Position = %i" % p.get_position() )
p.make_moves("LDDLRLRDDRLRUDDRDDUDRULUUULULDULRUULLRRDUULRDUUDDDRRULDDUDRLLLDULURDLDDRLLRURULULDLDULRDLDLRULUDLLDRUDLDURRDULDDRLRURDLLUDRDDDUDLUDULURULRDRLRULDLLRLDRRUDRDRUDRLDLRLUUURURRRLDDULLULLLRLRLULDLLRLDDRLDULURULRUURRUUURRUDRLRRURURDDDRULDULDLDLRRRLLDDRRURRULULULDRDULDRRULDUDRRLDULDRDURRDULLRRRLLLLRRLLRRRDRURDUULLURURURDDRRDRLLLULRRRDRLDRLDRDLLRUUDURRDRRDLLUDLDRLRLDLUDRDULRULRRLLRDLULDRLUDUUULLDRULDDLLRDUUUDRUUUUULUURDDLLDUURURRURLLURRDDUDUDRUUDDRDDRRLRLULRLRRRDRLLRRLLLDUULLUUDDLULLLDURRLLDRLDRDRLRRLRRULRRRRLRRRRRURUDULUULRDLLDRLRRDUURDRRUDRURRRDDRLDDLRLUDRDRDRRLDDDRDDRRRDUDULRURRDRDLLDRUD")
print("Position = %i" % p.get_position() )
p.make_moves("UUUDLDDLRDLLLLRUUURDDLLURRUUURLUULLURUUDUDLDULULLRRRRLLLRDLLUDRUURDRURUDRURRLRLDRURLUDRLULRRURDDDURLLDULDLRRRDUUDDDRDLRUURRDRDRLRDLULRLDDRULRULDRDUDRUURLDLUDDULLLRURRLURLULDRRLUUURURLDLDDULLLRUUURDDDUURULULLUUUDUDRLLRRULUULDDDLLUDLURLLLRRULLURDRLUUDDLLDLLLUDULLRDRRRURDRUDUDUULUDURDLRUDLLRDDRURUDURLRULURDDURULLRDDRLRRDRLLULRDDDULRDLRULDDLRRDULDLUURRURUULRRDUURUDRRRRRLDULDLRURRULULDLRDDDRLLDURRULDUDUDRRRLUULRLUDURRRLRLDURRRRUULDRLUDDDUDURLURUDLLUDRDDDRLLURLRLDDURUUDDDUDUR")
print("Position = %i" % p.get_position() )
p.make_moves("RURRRRURUDDRLURUDULRDUDDDUURULDRRRRURDLDRRLLDLUDLRRLRRUULLURULLRDLLRDDDDULLRLLDDLLRUDDULDUDLDURLRUULDDURURDURDLDRRULRURRRRRLRRLLUDURRURULRLRDLRLRRRLLURURDLLLDLDDULDLUDDLLLRUDDRDRLRUDRRLDDLRDLRLRLRLRRDUUURRUDRRLDLRRUULULLUDRRRUDLURDRUULDRDRRLUULULDDLURRLDULLURLDRLDULDRLLDLUUULLULRRDDRURRURLDLDRRLLLLLUDUURUULURLRDDDLRRRRLLLURUDLDDRDDRRUDURUULDRRULLLRRLRULLLRLDDLLRRLRURLRDRUDULLDDLDDDDDLDURURDLULRDDLRDLLRURLLRDLRUDDRDRRDURDURLUDRLDUDDDRRURRLUULURULLRLRDLRRLRURULLDDURLLRRRUDDRDLULURRRUUUULUULRRLLDLRUUURLLURLUURRLRL")
print("Position = %i" % p.get_position() )



