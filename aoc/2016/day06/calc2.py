# find the most frequently occurring character in each position
#
# each position should have a pointer to a 
#  dictionary- containing a char and a count
#
import operator


def update_stats(name):
    # is array entry populated?
    for i in range(0,len(name)):
        ch = name[i:i+1]
        if ncount[i] == 0:
            ncount[i] = {}
        counts_for_pos = ncount[i]
        if not ch in counts_for_pos:
            counts_for_pos[ch] = 0
        cur_count = counts_for_pos[ch]
        counts_for_pos[ch] = cur_count + 1
    print( ncount )
             

def show_max_repeating_chars():
    freq_chars = ''
    for i in range(0,len(ncount)):
        counts_for_pos = ncount[i]
        if counts_for_pos == 0:
            break;
        sorted_counts = sorted(counts_for_pos.items(),key=operator.itemgetter(1))
        num_counts = len(sorted_counts)
        freq_char = sorted_counts[0][0]
        freq_chars = freq_chars + freq_char
    print(freq_chars)


ncount = 1000*[0]


f = open('day6_input.txt', 'r')
for name in f:
    update_stats(name)

show_max_repeating_chars()

