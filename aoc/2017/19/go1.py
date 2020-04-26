from enum import Enum

class Direction(Enum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3


def get_step_in_direction(drtn):    
    if drtn == Direction.DOWN:
        return (1,0)
    if drtn == Direction.LEFT:
        return (0,-1)
    if drtn == Direction.RIGHT:
        return (0,1)
    if drtn == Direction.UP:
        return (-1,0)


def get_new_position(cur_y, cur_x, drtn):
    (dy, dx) = get_step_in_direction(drtn)
    return (cur_y+dy, cur_x+dx)


def test_new_position(new_y, new_x, maze):
    if new_y<0 or new_y>=len(maze):
        return False
    row = maze[new_y]
    if new_x<0 or new_x>=len(row):
        return False
    ch = maze[new_y][new_x]
    if ch == ' ':
        return False
    return True


def are_reverse_directions(current_heading, test_heading):
    if current_heading == Direction.DOWN and test_heading == Direction.UP:
        return True
    if current_heading == Direction.UP and test_heading == Direction.DOWN:
        return True
    if current_heading == Direction.LEFT and test_heading == Direction.RIGHT:
        return True
    if current_heading == Direction.RIGHT and test_heading == Direction.LEFT:
        return True
    return False
        


def scan_for_new_direction( cur_pos_y, cur_pos_x, current_dir, maze ):
    print('scan for new direction')
    for test_heading in range(0,4):
        test_dir = Direction(test_heading)
        if test_dir == current_dir or are_reverse_directions( current_dir, test_dir ):
            continue
        (new_y, new_x) = get_new_position(cur_pos_y, cur_pos_x, test_dir)
        if test_new_position(new_y, new_x, maze):
            return test_dir

    return -1



# translate input maze into memory array

def read_input():
    maze = []
    max_col = -1
    with open('data.txt', 'r') as file:
        data = file.read()
        for row in data.split('\n'):
            maze_row = []
            maze.append(maze_row)
            for idx in range(0, len(row)):
                ch = row[idx:idx+1]
                maze_row.append(ch)            
    return maze


def scan_for_entrance(row):
    for idx in range(0, len(row)):
        ch = row[idx:idx+1]
        print("%s (%s)" % (idx, ch))
        if ch[0] == '|':
            return idx
    return -1


def solve_maze(maze):
    idx = scan_for_entrance(maze[0])
    if idx < 0:
        return -1
    
    current_dir = Direction.DOWN
    cur_pos_x = idx
    cur_pos_y = 0

    cookies = []
    num_steps = 0
    while True:
        (cur_pos_y, cur_pos_x) = get_new_position( cur_pos_y, cur_pos_x, current_dir )
        print('pos yz = %s,%s' % (cur_pos_y, cur_pos_x) )
        if cur_pos_y<0 or cur_pos_y>len(maze):
            break
        if cur_pos_x<0 or cur_pos_x>len(maze[cur_pos_y]):
            break
        ch = maze[cur_pos_y][cur_pos_x]
        num_steps = num_steps + 1
        print('num steps = %s' % num_steps)
        if ch.isalpha():
            cookies.append(ch)
            print('reached %s' % ch)
            continue
        if ch == '+':
            current_dir = scan_for_new_direction( cur_pos_y, cur_pos_x, current_dir, maze )
    return cookies



maze = read_input()
print(''.join(solve_maze(maze)))