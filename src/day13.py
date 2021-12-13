
class Rect:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x, y) -> bool:
        return self.x <= x < self.width and self.y <= y < self.height

def dump_2d(arr2d:list):
    for row in arr2d:
        print(''.join(row))
    return

page_size = [0, 0]
points = set()
fold_queue = []

def fold_page(page_size: list, points: set, fold: tuple):
    x = 0
    y = 0
    w = page_size[0]
    h = page_size[1]
    
    if fold[0] == 'x':
        x = fold[1] + 1
    else:
        y = fold[1] + 1
    
    transformed = set()
    rect = Rect(x, y, w, h)
    for (next_x, next_y) in points:
        if (rect.contains(next_x, next_y)):
            # transformed
            if fold[0] == 'x':
                # x = 2; w = 5
                # (4, 0)
                # 0 1 [2] 3 4 
                pt = (fold[1] - (next_x - fold[1]), next_y)
                transformed.add(pt)
                page_size[0] = fold[1]
            else:
                pt = (next_x, fold[1] - (next_y - fold[1]))
                transformed.add(pt)
                page_size[1] = fold[1]
        else:
            transformed.add((next_x, next_y))
    return transformed

def part_1(page_size: list, points: set, fold_queue: list):
    front_fold = fold_queue.pop(0)
    points = fold_page(page_size, points, front_fold)
    return len(points)

def part_2(page_size: list, points: set, fold_queue: list):
    for front_fold in fold_queue:
        points = fold_page(page_size, points, front_fold)
    page = [['.'] * page_size[0] for x in range(page_size[1])]
    for x, y in points:
        page[y][x] = '#'
    dump_2d(page)
    

with open('../input/day13.txt') as istream:
    for line in istream:
        line = line.rstrip('\n')
        if len(line) == 0:
            continue
        if line.find(',') < 0:
            fold = line.split(' ')[2]
            axis, value = fold.split('=')
            fold_queue.append((axis, int(value)))
        else:
            x, y = [int(v) for v in line.split(',')]
            points.add((x, y))
            if page_size[0] < x + 1: page_size[0] = x + 1
            if page_size[1] < y + 1: page_size[1] = y + 1

print("Part_1: ", part_1(page_size.copy(), points.copy(), fold_queue.copy()))
print("Part_2: ", part_2(page_size, points, fold_queue))
