with open("test2.dat") as f:t = f.read()
q = [[int(j)+300 for j in i.split(", ")] for i in t.split("\n")[:-1]]
h = [sum(abs(x-i[0]) for i in q) for x in range(300,700)]
v = [sum(abs(y-i[1]) for i in q) for y in range(300,700)]
s = 0
for i in h:
    for j in v:
        if i+j < 10000: s+= 1
print(s)
