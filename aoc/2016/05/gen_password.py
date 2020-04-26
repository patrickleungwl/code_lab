

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

import hashlib


i=0
pw = ''
keep_going = True
while keep_going:
    idx = str(i)
    key = 'abbhdwsy' + idx
    val = hashlib.md5(key.encode('utf-8')).hexdigest()
    if val[0:5] == "00000":
        print("%i %s" % (i, val))
        pw = pw + val[5:6]
    i += 1
    if (len(pw)>=8):
        keep_going = False

print(pw)



