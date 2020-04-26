

def get_orders():
    file = open('input.txt','r')
    data = file.read()
    orders = []
    for row in data.split('\n'):
        orders.append(row)

    return orders



def execute_order(order, registers):
    parts = order.split(' ')
    cmd = parts[0]
    jump = 1

    if cmd == 'snd':
        reg = parts[1]
        if reg.isalpha():
            reg = int(registers[reg])
        else:
            reg = int(reg)
        print('snd %s' % reg)
        registers['snd'] = reg
    if cmd == 'set':
        reg = parts[1]
        val = parts[2]
        if val.isalpha():
            val = int(registers[val])
        else:
            val = int(val)
        registers[reg] = val
    if cmd == 'add':
        reg = parts[1]
        val = parts[2]
        if val.isalpha():
            val = int(registers[val])
        else:
            val = int(val)
        registers[reg] = registers[reg] + val
    if cmd == 'mul':
        reg = parts[1]
        val = parts[2]
        if val.isalpha():
            val = int(registers[val])
        else:
            val = int(val)
        registers[reg] = registers[reg] * val
    if cmd == 'mod':
        reg = parts[1]
        val = parts[2]
        if val.isalpha():
            val = int(registers[val])
        else:
            val = int(val)
        registers[reg] = registers[reg] % val
    if cmd == 'rcv':
        reg = parts[1]
        if reg.isalpha():
            reg = int(registers[reg])
        else:
            reg = int(reg)
        if reg != 0:
            print('recover %s' % registers['snd'])
            exit(0)
    if cmd == 'jgz':
        reg = parts[1]
        val = parts[2]

        if reg.isalpha():
            reg = int(registers[reg])
        else:
            reg = int(reg)

        if val.isalpha():
            val = int(registers[val])
        else:
            val = int(val)
        
        if reg != 0:
            jump = val

    return jump


def execute_orders(orders, registers):
    ip = 0
    while ip<len(orders)-1:
        order = orders[ip]
        jp = execute_order(order, registers)
        ip = ip + jp
        print(registers)
        print('ip, jp = %s, %s' % (ip, jp))
    print(registers)

def init_registers():
    registers = {}
    for i in range(0,25):
        c = chr(i+97)
        registers[c] = 0
    registers['a'] = 1
    return registers


registers = init_registers()
orders = get_orders()
execute_orders(orders, registers)

        







