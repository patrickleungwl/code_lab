import sys
import math
import datetime
import time

def parse_to_xy(str):
    beg = str.find('<')
    end = str.find('>')
    num = str[beg+1:end]
    xy = num.split(',')
    x = int(xy[0])
    y = int(xy[1])
    return (x,y)



def get_input(file_input):
    star_pos = []
    star_vel = []
    tmp = ' '
    with open(file_input) as f:
        while tmp:
            tmp = f.readline()
            if len(tmp)<2:
                continue
            vel_idx = tmp.find('vel')
            pos_str = tmp[0:vel_idx-1]
            vel_str = tmp[vel_idx:]
            (posx,posy) = parse_to_xy(pos_str)
            (velx,vely) = parse_to_xy(vel_str)
            star_pos.append((posx,posy))
            star_vel.append((velx,vely))

    return (star_pos,star_vel)


def move_stars(star_pos,star_vel):
    for i in range(0,len(star_pos)):
        (posx,posy) = star_pos[i]
        (velx,vely) = star_vel[i]
        posx = posx + velx
        posy = posy + vely
        star_pos[i] = (posx,posy)




def calc_block_distance(fromx,fromy,tox,toy):
    diffx = abs(tox-fromx)
    diffy = abs(toy-fromy)
    distance = diffx+diffy
    #print('%s,%s to %s,%s => %s' % (fromx,fromy,tox,toy,distance))
    return distance



def get_cumulative_distance_between_stars(star_pos):
    cumd = 0
    for s in star_pos:
        d = calc_block_distance(0,0,s[0],s[1])
        cumd = cumd + d
    return cumd


def show_stars(star_pos,i):
    # just show central -100,-100 to 100,100
    for y in range(200,300):
        row = ''
        for x in range(50,150):
            val = '.'
            for s in star_pos:
                posx = s[0]
                posy = s[1]
                if posx==x and posy==y:
                    val = '*' 
            row = row + val
        print(row)
    print(i)
    print('%s,%s' % (star_pos[0][0],star_pos[0][1])) 
    print('\n')



def show_cum_dist(cum_dist):
    for d in cum_dist:
        print(d) 



def show_star_area(star,star_pos,star_idx,turn_idx):
    starx = star[0]
    stary = star[1]
    num_close_stars = 0
    alert = ''
    for y in range(-20,20):
        row = ''
        adjy = stary+y
        for x in range(-50,50):
            val = '.'
            adjx = starx+x
            for s in star_pos:
                posx = s[0]
                posy = s[1]
                if posx==adjx and posy==adjy:
                    val = '*' 
                    num_close_stars = num_close_stars + 1
            row = row + val
        print(row)
    if num_close_stars > 20:
        alert = 'alert'
    print('Turn %s, Star %s, (%s,%s) %s' % (turn_idx,star_idx,starx,stary,alert))



def show_close_stars(star_pos,turn_idx):
    is_close = False
    for i in range(0,len(star_pos)):
        show_i_star_already = False
        for j in range(0,len(star_pos)):
            if i == j: 
                continue
            stara = star_pos[i]
            starb = star_pos[j]
            d = calc_block_distance(stara[0],stara[1],starb[0],starb[1])            
            if d < 3:
                if show_i_star_already == False:
                    show_star_area(star_pos[i],star_pos,i,turn_idx)
                    show_i_star_already = True

def is_stars_very_close(star_pos):
    is_close = False
    for i in range(0,len(star_pos)):
        for j in range(0,len(star_pos)):
            if i == j: 
                continue
            stara = star_pos[i]
            starb = star_pos[j]
            dist = calc_block_distance(stara[0],stara[1],starb[0],starb[1])            
            if dist < 10:
                is_close = True
                break
    return is_close


def animate_stars(star_pos,star_vel):
    i = 0
    cum_dist = []
    while i < 10400:
        if i > 10350 and i < 10383:
            show_close_stars(star_pos,i)
            #if is_stars_very_close(star_pos):
            show_stars(star_pos,i)
        move_stars(star_pos,star_vel)
        #cumd = get_cumulative_distance_between_stars(star_pos)
        #cum_dist.append(cumd)
        if i % 10:
            print(i)
        i = i+1
    

(star_pos,star_vel) = get_input(sys.argv[1])
animate_stars(star_pos,star_vel)

