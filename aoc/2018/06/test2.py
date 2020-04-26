from collections import defaultdict

 P = []
 for line in open('test2.dat'):
     x,y = [int(s.strip()) for s in line.split(',')]
     P.append((x,y))
 print len(P)

 xlo = min([x for x,y in P])
 xhi = max([x for x,y in P])
 ylo = min([y for x,y in P])
 yhi = max([y for x,y in P])
 print xlo, xhi
 print ylo, yhi

 def d((x1,y1), (x2,y2)):
     return abs(x1-x2) + abs(y1-y2)
 def closest(x,y):
     ds = [(d(p, (x,y)), p) for p in P]
     ds.sort()
     if ds[0][0] < ds[1][0]:
         return ds[0][1]
     else:
         return (-1,-1)

 def score_around(W):
     score = defaultdict(int)
     for x in range(xlo-W, xhi+W):
         for y in range(ylo-W, yhi+W):
             score[closest(x,y)] += 1
     return score

 S2 = score_around(400)
 S3 = score_around(600)

 best = [(S2[k] if S2[k]==S3[k] else 0, k) for k in S2.keys()]
 best.sort()
 for area, p in best:
     print area, p
