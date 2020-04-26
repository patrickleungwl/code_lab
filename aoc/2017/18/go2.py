
class Player:

    _orders = []
    _registers = {}
    _queue = []
    _id = -1
    _ip = 0

    def __init__(self, id):
        _orders = self.get_orders()
        _registers = self.init_registers(id)
        _id = id
        _ip = 0


    def init_registers(self, id):
        registers = {}
        for i in range(0,25):
            c = chr(i+97)
            registers[c] = 0
        registers['a'] = 1
        registers['p'] = id
        return registers


    def push_to_queue(job):
        _queue.append(job)


    def get_orders(self):
        with open('input.txt', 'r') as file:
            data = file.read()
            orders = []
            for row in data.split('\n'):
                orders.append(row)
            return orders


    def execute_order(other_player):

        if _ip<0 or _ip >= len(_orders):
            print('Player %s out at %s' % (_id, _ip))
            return

        order = _orders[_ip]
        parts = order.split(' ')
        cmd = parts[0]
        jump = 1
        did_send = 0
        #print('\n\n%s, %s' % (order,jump))

        if cmd == 'snd':
            reg = parts[1]
            if reg.isalpha():
                reg = int(registers[reg])
            else:
                reg = int(reg)
            print('snd%s %s' % (id, reg))
            other_player.push_to_queue(reg)
            did_send = 1
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
            if len(own_queue) > 0:
                val = own_queue.pop(0)
                registers[reg] = val
            else:
                print('Player %s nothing to receive' % (_id))
                return (0,0)

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

        return (jump, did_send)


def execute_orders(orders_1, orders_2, registers_1, registers_2):
    ip_1 = 0
    ip_2 = 0
    jp_1 = 0
    jp_2 = 0
    sent_1 = 0

    while 1:
        if ip_1<len(orders_1)-1:
            order = orders_1[ip_1]
            (jp_1, did_send) = execute_order(1, order, registers_1, queue_1, queue_2)
            ip_1 = ip_1 + jp_1
            sent_1 = sent_1 + did_send
            #print('1: %s' % registers_1)
            #print('1: ip_1=%s jp_1=%s' % (ip_1, jp_1))
        if ip_2<len(orders_2)-1:
            order = orders_2[ip_2]
            (jp_2, did_send) = execute_order(2, order, registers_2, queue_2, queue_1)
            ip_2 = ip_2 + jp_2
            #print('2: %s' % registers_2)
            #print('2: ip_2=%s jp_2=%s' % (ip_2, jp_2))
        #print('queue1: %s' % queue_1)
        #print('queue2: %s' % queue_2)

        if jp_1==0 and jp_2==0:
            print("Sent by 1 %s" % sent_1)
            return


p0 = Player(0)
p1 = Player(1)

        







