import sys

def get_input(file_input):
    input = []
    with open(file_input) as f:
        tmp = f.read()
        input = tmp.split()
    return input



def find_closest_match(input):
    for i in range(0,len(input)):
        for j in range(i+1,len(input)):
            # for each pair of strings, compare each char
            # if diff by more than 1, then no match
            left = input[i]
            right = input[j]
            num_diffs = 0
            for idx in range(0,len(left)):
                left_char = left[idx]
                right_char = right[idx]
                if left_char != right_char:
                    num_diffs = num_diffs + 1
                if num_diffs > 3:
                    break
            if num_diffs <= 2:
                print('%s and %s diff by %s' % (left, right, num_diffs))



input = get_input(sys.argv[1])
find_closest_match(input)

#cvgywxqubnuaefmsljdrpfzyi 
#cvgywxqubnuaefmsljdrpfzyi 
