import sys

def get_input(file_input):
    input = []
    with open(file_input) as f:
        tmp = f.read()
        input = tmp.split()
    return input


def has_frequency_counts(input,num_occurance):
    occurances = {}
    for i in range(0,len(input)):
        var = input[i]
        num_appeared = 0
        if var in occurances:
            num_appeared = occurances[var]
        occurances[var] = num_appeared + 1

    # which letter occurs exactly num_occurance times?
    for v in occurances.values():
        if v == num_occurance:
            return 1
    return 0


def show_freq_counts(input):
    two_score = 0
    three_score = 0
    for s in input:
        print(s)
        if has_frequency_counts(s,2):
            two_score = two_score + 1
        if has_frequency_counts(s,3):
            three_score = three_score + 1
        print('two=%s three=%s' % (two_score, three_score))

input = get_input(sys.argv[1])
show_freq_counts(input)


