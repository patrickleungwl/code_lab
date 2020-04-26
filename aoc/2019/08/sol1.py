import sys
import math

# mass, divide by 3, round down, subtract 2

def get_input(file):
    tmp = ''
    with open(file) as f:
        tmp = f.read()
    return tmp


def split_into_layers(input,dx,dy):
    num_pixs_per_frame = dx * dy
    st_frame=0
    cur_count=0
    pidx=0
    num0s=0 # keep count of 0s, 1s, and 2s per frame
    num1s=0 # each frame is num_pix_per_frame
    num2s=0
    layer=0
    num0s_frame=[]
    num1s_frame=[]
    num2s_frame=[]
    with open('output.txt','w') as f:
        while True:
            if pidx >= len(input):
                break
            p = input[pidx]
            if p == '0':
                num0s = num0s + 1
            if p == '1':
                num1s = num1s + 1
            if p == '2':
                num2s = num2s + 1
            pidx = pidx + 1
            cur_count = cur_count + 1
            if cur_count >= num_pixs_per_frame: 
                num0s_frame.append(num0s)
                num1s_frame.append(num1s)
                num2s_frame.append(num2s)
                f.write('[%5i] %s\n' % (num0s, input[st_frame:st_frame+num_pixs_per_frame])) 
                print('[%5i] %s\n' % (num0s, input[st_frame:st_frame+num_pixs_per_frame])) 
                st_frame=pidx
                num0s=0
                num1s=0
                num2s=0
                cur_count=0

    # find frame with fewest 0s
    num_zeros=100000
    frame_zero=-1
    for i in range(0,len(num0s_frame)):
        if num0s_frame[i] < num_zeros:
            num_zeros = num0s_frame[i]
            frame_zero=i

    print('frame %i has %i zeros' % (frame_zero, num_zeros))
    num1 = num1s_frame[frame_zero]
    num2 = num2s_frame[frame_zero]
    print('%i x %i = %i' % (num1, num2, num1*num2))





input = get_input('input.txt')
split_into_layers(input,25,6)

