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
    frames=[]
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
                frames.append(input[st_frame:st_frame+num_pixs_per_frame])
                print('[%5i] %s\n' % (num0s, input[st_frame:st_frame+num_pixs_per_frame])) 
                st_frame=pidx
                num0s=0
                num1s=0
                num2s=0
                cur_count=0
    return frames

# 0 is black
# 1 is white
# 2 is transparent

def decode_frames(frames):
    final=[]
    # let's go thru each pixel of each frame
    for pidx in range(0,len(frames[0])):
#    for pidx in range(0,1):
        # start from 0 to final frame
        fidx=0
        color = 2
        while True:
            if fidx >= len(frames):
                break
            fr = frames[fidx]
            color = fr[pidx:pidx+1]
            #print('%i %s' % (fidx,color))
            if color == '0' or color == '1':
                break
            fidx = fidx + 1

        #print('final %s' % (color))
        final.append(color)
    print(''.join(final))


#input = get_input('input.txt')
#frames = split_into_layers(input,25,6)
frames = split_into_layers('0222112222120000',2,2)
decode_frames(frames)

