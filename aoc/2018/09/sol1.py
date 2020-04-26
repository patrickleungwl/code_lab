import sys
import datetime 


def get_seventh_left_location(num_items, cur_location):
    for i in range(0,7):
        cur_location = get_left_location(num_items, cur_location)
    return cur_location


def get_left_location(num_items, cur_location):
    if num_items <= 1:
        return 0

    new_location = cur_location - 1
    if new_location < 0:
        new_location = num_items-1

    return new_location


def get_new_location(num_items, cur_location):
    if num_items <= 1:
        return 0

    new_location = cur_location + 1
    if new_location >= num_items:
        new_location = 0

    return new_location


def add_new_marble(num_marbles, cur_location):
    # marbles is a list of marbles
    # find new place in list of marbles
    if num_marbles == 0:
        return 0
    if num_marbles == 1:
        return 1

    move1 = get_new_location(num_marbles, cur_location)
    return move1 + 1


assert get_new_location(0,0) == 0, 'Start location 0'
assert get_new_location(1,0) == 0, 'Start location 1'
assert get_new_location(2,1) == 0, 'Start location 2'
assert get_left_location(2,0) == 1, 'Left location 1'
assert get_left_location(3,1) == 0, 'Left location 2'
assert get_seventh_left_location(23,13) == 6, 'Left location test'
assert get_new_location(2,1) == 0, 'Start location 2'
assert add_new_marble(0,0) == 0, 'Add marble 0'
assert add_new_marble(1,0) == 1, 'Add marble 1'
assert add_new_marble(2,1) == 1, 'Add marble 2'
assert add_new_marble(3,1) == 3, 'Add marble 3'
assert add_new_marble(4,3) == 1, 'Add marble 4'
assert add_new_marble(5,1) == 3, 'Add marble 5'
assert add_new_marble(7,5) == 7, 'Add marble 7'
assert add_new_marble(9,1) == 3, 'Add marble 9'

num_players = 427
max_marble = 7072400
cur_location = 0
tricky_multiple = 23
marbles = [0]
scores = {}
for i in range(1,max_marble):
    if i % 10000 == 0:
        print(i)

    nth_player = i % num_players
    if nth_player == 0:
        nth_player = num_players

    if i % tricky_multiple == 0:
        if not nth_player in scores:
            scores[nth_player] = 0
        scores[nth_player] = scores[nth_player] + i
        left_location = get_seventh_left_location(len(marbles),cur_location)
        left_location_score = marbles[left_location]
        scores[nth_player] = scores[nth_player] + left_location_score
        marbles.pop(left_location)
        cur_location = left_location
    else:
        new_location = add_new_marble(len(marbles), cur_location)
        marbles.insert(new_location, i)
        cur_location = new_location
    #print('[%s] %s' % (nth_player, marbles))

print(max(scores.values()))
