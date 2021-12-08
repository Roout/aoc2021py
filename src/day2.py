# aim
x = 0
y = 0
depth = 0
shift = { 'forward': (1, 0), 'down': (0, 1), 'up': (0, -1) }
with open('../input/day2.txt', 'r') as istream:
    for line in istream:
        (key, value) = line.split()
        if key == 'forward':
            depth += y * int(value)
        x += shift[key][0] * int(value)
        y += shift[key][1] * int(value)
print(x * depth)