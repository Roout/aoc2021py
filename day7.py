
def accumulate(values, fn):
    mn, mx = min(values), max(values)
    lowest_cost = None
    for pivot in range(mn, mx + 1):
        cost = 0
        for crab in values:
            cost += fn(crab, pivot)
        if lowest_cost == None or lowest_cost > cost: 
            lowest_cost = cost
    return lowest_cost

def part_1(values):
    return accumulate(values, lambda a, b: abs(a - b))

def arithmetic_sum(a, b):
    n = abs(a - b)
    return (n * (1 + n)) >> 1

def part_2(values):
    return accumulate(values, arithmetic_sum)

values = []
with open('input/day7.txt', 'r') as istream:
    values = [ int(n) for n in istream.readline().split(',') ]

print("Part_1: ", part_1(values))
print("Part_2: ", part_2(values))