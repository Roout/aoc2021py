
def part_1(count_by_timer):
    max_age = 8
    for day in range(80):
        add = [0 for x in range(max_age + 1)]
        for timer in range(max_age + 1):
            fish_count = count_by_timer[timer]
            next_timer = timer - 1 if timer else 6
            add[timer] -= fish_count
            add[next_timer] += fish_count 
            if timer == 0:
                add[max_age] += fish_count
        for timer in range(max_age + 1):
            count_by_timer[timer] += add[timer]
    return sum(count_by_timer)

def part_2(count_by_timer):
    max_age = 8
    for day in range(256):
        add = [0 for x in range(max_age + 1)]
        for timer in range(max_age + 1):
            fish_count = count_by_timer[timer]
            next_timer = timer - 1 if timer else 6
            add[timer] -= fish_count
            add[next_timer] += fish_count 
            if timer == 0:
                add[max_age] += fish_count
        for timer in range(max_age + 1):
            count_by_timer[timer] += add[timer]
    return sum(count_by_timer)


# count of fish with the given timer
count_by_timer = [0 for x in range(9)]
with open('../input/day6.txt', 'r') as istream:
    timers = [int(n) for n in istream.readline().rstrip('\n').split(',')]
    for timer in timers:
        count_by_timer[timer] += 1

print('Part 1: ', part_1(count_by_timer.copy()))
print('Part 2: ', part_2(count_by_timer.copy()))
