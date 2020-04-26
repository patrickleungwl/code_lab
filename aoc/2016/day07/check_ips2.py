
'''
An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere 
in the supernet sequences (outside any square bracketed sections), and a 
corresponding Byte Allocation Block, or BAB, anywhere in the hypernet 
sequences. An ABA is any three-character sequence which consists of the same 
character twice with a different character between them, such as xyx or aba. 
A corresponding BAB is the same characters but in reversed positions: yxy and 
bab, respectively.

For example:

    aba[bab]xyz supports SSL (aba outside square brackets with corresponding 
        bab within square brackets).
    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in 
        hypernet; the aaa sequence is not related, because the interior character must be different).
    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a 
       corresponding bzb, even though zaz and zbz overlap).

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
        ip = ip.replace(inside_str, 'patrick' )
    ip = ip.replace('[patrick]',':')
    result = ip.split(':')
    return result


def get_all_abas(outside_strings):
    result = []
    for ostr in outside_strings:
        for i in range(0,len(ostr)-2):
            starting_char = ostr[i:i+1]
            ending_char = ostr[i+2:i+3]
            if starting_char == ending_char:
                result.append(ostr[i:i+3])
    return result


def babs_exist(inside_strings, abas):
    for aba in abas:
        'aba --> bab'
        bab_to_find = aba[1] + aba[0] + aba[1]
        print('     From %s, looking for %s' % (aba, bab_to_find))
        for istr in inside_strings:
            if istr.find(bab_to_find)>=0:
                print('     Found ' + bab_to_find)
                return True
    return False


def check_ips(ip):
    print('Checking ' + ip )
    inside_bracket_strings = get_inside_bracketed_strings(ip)
    outside_bracket_strings = get_outside_bracketed_strings(ip, inside_bracket_strings)
    abas = get_all_abas(outside_bracket_strings)
    return babs_exist(inside_bracket_strings, abas)

'''
print(check_ips('aba[bab]xyz'))
print(check_ips('xyx[xyx]xyx'))
print(check_ips('aaa[kek]eke'))
print(check_ips('zazbz[bzb]cdb'))
'''

f = open('input.txt','r')
for line in f:
    if check_ips(line):
        print(line)




