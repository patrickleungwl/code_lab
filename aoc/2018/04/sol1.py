import sys
import numpy as np
import datetime 

def get_input(file_input):
    input = []
    with open(file_input) as f:
        tmp = f.read()
        input = tmp.split('\n')
    return input


def parse_input(input):
    if len(input)<2:
        return

    dt = input[1:17]
    dtobj = datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M')
    datestr = dtobj.date().isoformat()

    if input.find('Guard')>-1:
        # get the guard id
        idx = input[26:].find(' ')
        guardstr = input[26:26+idx]
        if dtobj.time().hour > 4:
            tdelta = datetime.timedelta(days=1)
            nextday = dtobj + tdelta
            datestr = nextday.date().isoformat()

        print('Guard [%s] on [%s]' % (guardstr,datestr))
        date_guard[datestr] = guardstr
        date_record[datestr] = np.zeros((1,60))

    # asleep state is 1
    # awake state is 0 

    minute = dtobj.time().minute

    if input.find('falls')>-1:
        # mark everything to the right of minute as sleeping
        for i in range(minute,60):
            date_record[datestr][0,i] = 1

    if input.find('wakes')>-1:
        # mark everything to the right of minute as awake
        for i in range(minute,60):
            date_record[datestr][0,i] = 0



def find_guard_that_sleeps_most():
    print('finding')
    guard_sleep_totalmins={}
    guard_sleep_record={}
    for datestr, guard in date_guard.items():
        if not guard in guard_sleep_totalmins:
            guard_sleep_totalmins[guard]=0
            guard_sleep_record[guard]=np.zeros((1,60))
        sleep_mins = guard_sleep_totalmins[guard]
        tmp_sleep_record = guard_sleep_record[guard]

        mins_asleep = 0
        sleep_record = date_record[datestr]
        #print('%s %s' % (datestr,sleep_record))
        for i in range(0,60):
            if sleep_record[0,i] == 1:
                mins_asleep = mins_asleep+1
                tmp_sleep_record[0,i] = tmp_sleep_record[0,i]+1

        sleep_mins = sleep_mins + mins_asleep
        #print('Guard %s slept %s min' % (guard,sleep_mins))
        guard_sleep_totalmins[guard] = sleep_mins

    maxmins = 0
    maxguard = -1
    for guard, totalmins in guard_sleep_totalmins.items():
        if totalmins > maxmins: 
            maxguard = guard
            maxmins = totalmins
    print('Guard that slept most ', maxguard)

    # what minute did this guard sleep the most?
    sleep_record = guard_sleep_record[maxguard]
    min_slept_most = -1
    times_slept = 0
    for i in range(0,60):
        if sleep_record[0,i]>times_slept:
            times_slept = sleep_record[0,i]
            min_slept_most = i
    print('The Minute slept most by guard = ', min_slept_most)

    # for all guards, which minute did was asleep most?

    max_guard=-1
    max_times_slept = 0
    keep_minute_slept = -1
    for guard in guard_sleep_record.keys():
        sleep_record = guard_sleep_record[guard]

        min_slept_most = -1
        times_slept = 0
        for i in range(0,60):
            if sleep_record[0,i]>times_slept:
                times_slept = sleep_record[0,i]
                min_slept_most = i
        
        if times_slept > max_times_slept: 
            max_times_slept = times_slept
            max_guard = guard
            keep_minute_slept = min_slept_most

    print('Guard %s slept most the minute %s' % (max_guard, keep_minute_slept))




date_guard = {}
date_record = {}
input = get_input(sys.argv[1])
sinput = sorted(input)
for inp in sinput:
    parse_input(inp)

find_guard_that_sleeps_most()

