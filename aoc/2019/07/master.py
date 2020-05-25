import os

nsend = 'm_s'
nreceive = 's_m'

if not os.path.exists(nsend):
    print('making nsend')
    os.mkfifo(nsend)
if not os.path.exists(nreceive):
    print('making nreceive')
    os.mkfifo(nreceive)

psend = os.open(nsend, os.O_WRONLY)
preceive = os.open(nreceive, os.O_RDONLY)

for i in range(0,20):
    os.write(psend,'%s' % i)
    stdt = os.read(preceive,2)
    print(stdt)

os.write(psend,'x')
os.unlink(nsend)
os.unlink(nreceive)


