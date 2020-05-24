# say_my_name.py
import sys
print "what's your name?"
for name in iter(sys.stdin.readline, ''):
    name = name[:-1]
    if name == "exit":
        break
    print "Well how do you do {0}?".format(name)
    print "what's your name?"
