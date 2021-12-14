
def assign_or_modify(d: dict, key, value):
    if key not in d:
        d[key] = value
    else:
        d[key] += value

def part_1(template: str, rules: dict):
    counter = {}
    # init starting state
    state = {}
    assign_or_modify(counter, template[0], 1)
    for i in range(1, len(template)):
        assign_or_modify(state, template[i - 1: i + 1], 1)
        assign_or_modify(counter, template[i], 1)
    # simulate
    steps = 10
    for i in range(steps):
        # { polimer: count }
        added_polimers = {}
        for polimer, ins in rules.items():
            if polimer in state:
                keys = [
                    ''.join([polimer[0], ins]),
                    ''.join([ins, polimer[1]]),
                ]
                count = state[polimer]
                assign_or_modify(counter, ins, count)
                assign_or_modify(added_polimers, keys[0], count)
                assign_or_modify(added_polimers, keys[1], count)
                state[polimer] = 0
        # copy to updated state
        for polimer, count in added_polimers.items():
            assign_or_modify(state, polimer, count)
        added_polimers.clear()
    
    min = 1 << 64
    max = 0
    for v in counter.values():
        if v < min: min = v
        if v > max: max = v
    return max - min

template = str()
rules = {}

with open('../input/day14.txt') as istream:
    template = istream.readline().rstrip('\n')
    istream.readline() # skip
    for line in istream:
        key, val = line.rstrip('\n').split(' -> ')
        assert(key not in rules)
        rules[key] = val
print('Part_1: ', part_1(template, rules))
