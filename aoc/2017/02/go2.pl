# It sounds like the goal is to find the only two numbers in 
# each row where one evenly divides the other - that is, where 
# the result of the division operation is a whole number. 
# They would like you to find those numbers on each line, 
# divide them, and add up each line's result.
#
#For example, given the following spreadsheet:
#
#5 9 2 8
#9 4 7 3
#3 8 6 5
#
#    In the first row, the only two numbers that evenly 
#    divide are 8 and 2; the result of this division is 4.
#    In the second row, the two numbers are 9 and 3; the result is 3.
#    In the third row, the result is 2.
#
#In this example, the sum of the results would be 4 + 3 + 2 = 9.
#
import sys
import math

file = open('data.txt', 'r')
data = file.read()
rows = data.split('\n')
sum = 0
for row in rows:
    if len(row)==0:
        break
    print(row)
    nums = row.split('\t')
    for ac in nums:
        a = int(ac)
        for bc in nums:
            b = int(bc)
            if a==b:
                continue
            if a % b == 0:
                diff = int(a/b) 
                print("%s %s %s" % (a, b, diff))
                sum = sum + diff

print(sum)


