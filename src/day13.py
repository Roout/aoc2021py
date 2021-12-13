
def dump_2d(arr2d:list):
    for row in arr2d:
        print(row)
    return

SIZE = 15
page = [['.'] * SIZE for x in range(SIZE)]
fold_queue = []

with open('../input/day13.txt') as istream:
    for line in istream:
        line = line.rstrip('\n')
        if len(line) == 0:
            print("Empty line")
            continue
        if line.find(',') < 0:
            fold = line.split(' ')[2]
            axis, value = fold.split('=')
            fold_queue.append((axis, int(value)))
        else:
            x, y = [int(v) for v in line.split(',')]
            page[y][x] = '#'

dump_2d(page)
print(fold_queue)

