import sys

# python3 keys, values, items

def test_dict_loops(input):
    for k in input:
        print(k)
    print('\n')

    for k in input.keys():
        print(k)
    print('\n')

    for k in input.keys():
        print(k)
    print('\n')

    for v in input.values():
        print(v)
    print('\n')

    for k, v in input.items():
        print(k,v)
    print('\n')


input = {}
input['abcd'] = 1
input['abcde'] = 2
input['abcdf'] = 3

test_dict_loops(input)

