def init_elves(num_elves):
    e = []
    for i in range(0,num_elves):
        e.append(i)
    return e


def put_str_in_list(str): 
    r = []
    for idx in range(0,len(str)):
        i = int(str[idx])
        r.append(i)
    return r


def get_recipe_sum(r,e):
    sum = 0
    for i in range(0,len(e)):
        loc = e[i]
        sum = sum + r[loc] 
    return sum


def add_num_digits_to_recipe(r,num):
    numstr = str(num)
    r.extend(put_str_in_list(numstr))
    return r



def get_num_recipe(lt):
    num_recipes = len(lt)-10
    if num_recipes < 0:
        num_recipes = 0
    return num_recipes


def pretty_short_list(lt):
    num_recipes = get_num_recipe(lt)
    #sum_str = '[%s]' % (num_recipes)
    sum_str=''
    for i in range(num_recipes,len(lt)):
        num = lt[i]
        sum_str = sum_str + str(num)
    return sum_str


def pretty_list(lt):
    sum_str = ''
    for i in lt:
        sum_str = sum_str + ' ' + str(i)
    return sum_str


def move_elves(e,r):
    for i in range(0,len(e)):
        # move ith elf
        loc = e[i]
        value = r[loc]
        num_steps = value + 1
        new_loc = (loc + num_steps) % len(r)
        e[i] = new_loc
    return e


input = '37'
e = init_elves(2)
r = put_str_in_list(input)
i = 0
while True:
    sum = get_recipe_sum(r,e)
    r = add_num_digits_to_recipe(r,sum)
    e = move_elves(e,r)
    n = get_num_recipe(r)

    list_str = pretty_short_list(r)
    #print('%s (%s)' % (list_str, pretty_list(e)))

    i = i+1
    if i % 100000 == 0:
        print('%s' % (i))

    #if list_str[0:5] == '59414':
    #    print('%s %s ' % (n,list_str[0:5]))
    #    exit(0)
    
    if list_str[0:6] == '909441':
        print('%s %s ' % (n,list_str[0:6]))
        exit(0)

