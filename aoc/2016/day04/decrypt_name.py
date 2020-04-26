import operator


def rotate_character(ch, num):
    # move c forward n number of times
    # a moved 3 times forward = b c d, d
    # z moved 3 times forward = a b c, c
   
    # a = 97, z = 122
    real_moves = num % 26
    idx = ord(ch)
    idx += real_moves
    if (idx > 122):
        idx = idx-26
    return chr(idx)


def decrypt_room_name(name):
    id = get_sector_id(name)
    decrypted = ''
    nameparts = name.split('-')
    for i in range(0,len(nameparts)-1):
        word = nameparts[i]
        # rotate each letter id number of times
        decrypted_word = ''
        for ch in word:
            decrypted_word = decrypted_word + rotate_character(ch,id)
        if len(decrypted)>0:
            decrypted = decrypted + ' ' + decrypted_word
        else:
            decrypted = decrypted_word
    return decrypted


def get_sector_id(name):
    first_digit = ''
    for n in name:
        if n.isdigit():
            first_digit = n
            break
    id_idx = name.find(first_digit)
    checksum_idx = name.find('[')
    sector_id = name[id_idx:checksum_idx]
    return int(sector_id)



def is_real_room_name(name):
    # is real roo name if checksum
    # shows the top 5 occurring alphabet used in room name
    # ties are broken by alphabetic order
    # 
    counts = {}
    first_digit = ''
    for n in name:
        if n.isalpha():
            if not n in counts:
                counts[n] = "10000:%s" % (n)
            value = counts[n]
            values = value.split(':')
            count = int(values[0])
            count -= 1
            value = "%05i:%s" % (count, n)
            counts[n] = value
        if n.isdigit():
            first_digit = n
            break

    id_idx = name.find(first_digit)
    checksum_idx = name.find('[')
    checksum_end_idx = name.find(']')
    checksum = name[checksum_idx+1:checksum_end_idx]

    sorted_n = sorted(counts.items(), key= operator.itemgetter(1) )
    calced_checksum = ''
    for idx in range(0,5):
        calced_checksum += sorted_n[idx][0]

    print(calced_checksum)
    if calced_checksum == checksum:
        return True
    return False


#print(get_sector_id('aaaaa-bbb-z-y-x-123[abxyz]'))
#is_real_room_name('aaaaa-bbb-z-y-x-123[abxyz]')
#is_real_room_name('a-b-c-d-e-f-g-h-987[abcde]')
#is_real_room_name('not-a-real-room-404[oarel]')
#is_real_room_name('totally-real-room-200[decoy]')


total_sector_ids = 0
f = open('day4_input.txt', 'r')
for name in f:
    if is_real_room_name(name):
        print("%s is real" % name )
        total_sector_ids += get_sector_id(name)
        print("decrypted: %s" % decrypt_room_name(name))
    else:
        print("%s is not real" % name )

print(total_sector_ids)



