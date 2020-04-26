
'''
An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. 
An ABBA is any four-character sequence which consists of a pair of two different 
characters followed by the reverse of that pair, such as xyyx or abba. However, 
the IP also must not have an ABBA within any hypernet sequences, which are 
contained by square brackets.

For example:

    abba[mnop]qrst supports TLS (abba outside square brackets).
    abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).
'''

def get_char_pair(ip, pos, idx):
    if pos+idx>len(ip):
        return ('ab')
    return ip[pos+idx:pos+idx+2]


def get_inside_bracketed_strings(ip):
    keep_searching = True
    idx = 0
    result = []
    while keep_searching:
        start_idx = ip.find('[', idx)
        if start_idx > 0:
            end_idx = ip.find(']', start_idx)
            idx = end_idx
            result.append( ip[start_idx+1:end_idx] )
        else:
            keep_searching = False
    return result



def get_outside_bracketed_strings(ip, inside_strings):
    keep_searching = True
    idx = 0
    result = []
    for inside_str in inside_strings:
        ip = ip.replace(inside_str, 'XZXZXZXZ' )
    ip = ip.replace('[XZXZXZXZ]',':')
    result = ip.split(':')
    return result


def check_ips_in_string(ip):
    for i in range(0,len(ip)):
        char_pair = get_char_pair(ip, i, 0)
        next_char_pair = get_char_pair(ip, i, 2)
        if char_pair == next_char_pair:
            continue 
        if char_pair == next_char_pair[::-1]:
            return True
    return False


def check_ips(ip):
    print('Checking ' + ip )
    inside_bracket_strings = get_inside_bracketed_strings(ip)
    outside_bracket_strings = get_outside_bracketed_strings(ip, inside_bracket_strings)
    for inner in inside_bracket_strings:
        print('     Checking inside ' + inner )
        if check_ips_in_string(inner):
            print("     False")
            return False
    for outer in outside_bracket_strings:
        print('     Checking ' + outer )
        if check_ips_in_string(outer):
            print('     True')
            return True
    print('     False')
    return False


'''
insides = get_inside_bracketed_strings('jkkafippjksskunza[nzdfqunmpbdigxgfn]qtofhensduhghfgred[erdtqivhpppgnkmldd]figxwdiqmlzocmngh')
print(insides)
print(get_outside_bracketed_strings('jkkafippjksskunza[nzdfqunmpbdigxgfn]qtofhensduhghfgred[erdtqivhpppgnkmldd]figxwdiqmlzocmngh', insides))

print(check_ips('abba[mnop]qrst'))
print(check_ips('abcd[bddb]xyyx'))
print(check_ips('aaaa[qwer]tyui'))
print(check_ips('ioxxoj[asdfgh]zxcvb'))
print(check_ips('jkkafippjksskunza[nzdfqunmpbdigxgfn]qtofhensduhghfgred[erdtqivhpppgnkmldd]figxwdiqmlzocmngh'))
'''

f = open('input.txt','r')
for line in f:
    if check_ips(line):
        print(line)
