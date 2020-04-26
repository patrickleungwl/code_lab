#

def rotate_3x3(sq):

    # assert sq is 3x3
    if len(sq) != 3:
        print('Wrong sq size')
        return ''

    newsq = []
    row1 = [ sq[0][2], sq[1][2], sq[2][2] ]
    row2 = [ sq[0][1], sq[1][1], sq[2][1] ]
    row3 = [ sq[0][0], sq[1][0], sq[2][0] ]
    newsq.append(row1)
    newsq.append(row2)
    newsq.append(row3)
    return newsq


def stream_sq(sq):
    result = ''
    for r in range(0,len(sq)):
        for c in range(0,len(sq[r])):
            result += (sq[r][c])
        if r < len(sq)-1:
            result += '/'
    return result


#  ABC   CFI   IHG   GDA
#  DEF   BEH   FED   HEB
#  GHI   ADG   CBA   IFC
testrow1 = ['A','B','C']
testrow2 = ['D','E','F']
testrow3 = ['G','H','I']
testsq = []
testsq.append(testrow1)
testsq.append(testrow2)
testsq.append(testrow3)

for idx in range(0,4):
    testsq = rotate_3x3(testsq)
    print(stream_sq(testsq))

