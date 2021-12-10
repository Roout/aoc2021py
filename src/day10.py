
from functools import reduce


def find_first_error(seq: str):
    stack = []
    open_by_close = { ')': '(', '}': '{', ']': '[', '>': '<' }
    for ch in seq:
        if ch in open_by_close:
            if len(stack) == 0: 
                return (ch, stack)
            back = stack.pop()
            if open_by_close[ch] != back:
                return (ch, stack)
        else:
            stack.append(ch)
    return (None, stack)

def part_1(input):
    errors = { ')': 0, '}': 0,    ']': 0,  '>': 0 }
    points = { ')': 3, '}': 1197, ']': 57, '>': 25137 }
    for line in input:
        res = find_first_error(line.rstrip('\n'))[0]
        if res != None:
            errors[res] += 1
    s = 0
    for (item, count) in errors.items():
        s += count * points[item]
    return s


def part_2(input):
    points = { ')': 1, '}': 3, ']': 2, '>': 4 }
    close_by_open = { '(': ')', '{': '}', '[': ']', '<': '>' }
    total = []
    for line in input:
        ch, stack = find_first_error(line.rstrip('\n'))
        if ch == None:
            stack.reverse()
            total += [reduce(lambda init, val: 5 * init + points[close_by_open[val]], stack, 0)]
    total.sort()
    return total[int(len(total) / 2)]

with open('../input/day10.txt') as istream:
    input = istream.readlines()
    print('Part_1: ', part_1(input))
    print('Part_2: ', part_2(input))