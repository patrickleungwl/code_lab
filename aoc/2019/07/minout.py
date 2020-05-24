import subprocess as sp
import time

args = './inout.py'
p = sp.Popen(args,stdin=sp.PIPE,stdout=sp.PIPE)
#p = sp.Popen(args)
print('before open comm')

outs, errs = p.communicate(input='4')
print(outs)
outs, errs = p.communicate(input='hey')
print(outs)
outs, errs = p.communicate(input='exit')

#p.stdin.write('4')
#result = p.stdout.read()
#print(result)


