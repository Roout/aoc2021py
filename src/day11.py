
def calc_flashlights(map):
    s = 0
    for r in map:
        for v in r:
            s += 1 if v == 0 else 0
    return s

def is_sync(map):
    val = map[0][0]
    for r in map:
        for v in r:
            if v != val:
                return False
    return True

def simulate(map):
    MAX = 9
    dx = [-1, -1,  0, 1, 1,  1,  0, -1]
    dy = [ 0,  1,  1, 1, 0, -1, -1, -1]
    HEIGHT = len(map)
    assert(HEIGHT > 0)
    WIDTH  = len(map[0])
    flashed = [[False] * WIDTH for row in range(HEIGHT)]
    que = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if map[y][x] == MAX:
                assert(flashed[y][x] == False)
                que.append((x, y))
                flashed[y][x] = True
                map[y][x] = 0
                while len(que) > 0:
                    cur_x, cur_y = que.pop(0)
                    for i in range(len(dx)):
                        next_y = cur_y + dy[i]
                        next_x = cur_x + dx[i]
                        if 0 <= next_x < WIDTH and 0 <= next_y < HEIGHT:
                            if flashed[next_y][next_x] == True:
                                continue
                            if map[next_y][next_x] == MAX:
                                que.append((next_x, next_y))
                                flashed[next_y][next_x] = True
                                map[next_y][next_x] = 0
                            else:
                                map[next_y][next_x] += 1                           
            elif flashed[y][x] == False:
                map[y][x] += 1
    pass

def part_1(input):
    # make list
    map = [[int(x) for x in line] for line in input]
    s = 0
    for i in range(100):
        simulate(map)
        s += calc_flashlights(map)
    return s

def part_2(input):
     # make list
    map = [[int(x) for x in line] for line in input]
    iter = 0
    while is_sync(map) == False:
        simulate(map)
        iter += 1
    return iter

with open('../input/day11.txt') as istream:
    input = [line.rstrip('\n') for line in istream.readlines() ]
    print("Part_1: ", part_1(input))
    print("Part_2: ", part_2(input))