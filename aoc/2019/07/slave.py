import os

nsend = 's_m'
nreceive = 'm_s'

preceive = os.open(nreceive, os.O_RDONLY)
psend = os.open(nsend, os.O_WRONLY)

while True:
    pin = os.read(preceive,2)
    if pin == 'x':
        break
    num_input = int(pin)
    os.write(psend, '%s' % (num_input*2))
