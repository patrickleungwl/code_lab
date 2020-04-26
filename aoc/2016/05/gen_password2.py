

# generate password from door id
#
# if an index starts with five zeros, the sixth char is the 
# next character in the password
#
# abc[idx] 
# abc3231929 first time first five chars are zero
# keep the 6th char - first char of pw
# abc5017308 second time first five chars are zer
# keep the 6th char - keep going
# until all 8 pw chars are found
#
# sixth character = position
# seventh character = pw char
# skip if position > 7

import hashlib

i=0
cnt=0
pw = 8 * ['']
while cnt<8:
    idx = str(i)
    key = 'abbhdwsy' + idx
    val = hashlib.md5(key.encode('utf-8')).hexdigest()
    if val[0:5] == "00000":
        print("%i %s" % (i, val))
        pos_char = val[5:6]
        if pos_char.isnumeric():
            pos = int(pos_char)
            pw_char = val[6:7]
            if pos < 8:
                if pw[pos] == '':
                    pw[pos] = pw_char
                    cnt += 1
                    print("  %s %i" % (pw, cnt))
    i += 1

print(pw)



