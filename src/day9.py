
from typing import Callable


dx = [-1, 1, 0,  0]
dy = [ 0, 0, 1, -1]

def in_bounds(map, x, y):
    height = len(map)
    assert(height > 0)
    width = len(map[0])
    return 0 <= x < width and 0 <= y < height

def apply_to_lowest(map, init, fn: Callable):
    width = len(map[0])
    height = len(map)
    for i in range(height):
        for j in range(width):
            is_lowest = True
            for k in range(4):
                x = dx[k] + j
                y = dy[k] + i
                if in_bounds(map, x, y) and map[i][j] >= map[y][x]:
                    is_lowest = False
                    break
            if is_lowest:
                init += fn(x = j, y = i)
    return init

def Bfs(map, start:tuple):
    WALL = 9

    height = len(map)
    width = len(map[0])
    
    basin_size = 0
    used = [[False] * width for row in range(height)]
    que = [start]
    used[start[1]][start[0]] = True
    while len(que) > 0:
        x, y = que.pop(0)
        basin_size += 1
        for k in range(4):
            next_x = dx[k] + x
            next_y = dy[k] + y
            if in_bounds(map, next_x, next_y) and used[next_y][next_x] == False:
                if map[next_y][next_x] != WALL and map[next_y][next_x] > map[y][x]:
                    que.append((next_x, next_y))
                    used[next_y][next_x] = True
    return basin_size                

def part_1(map):
    return apply_to_lowest(map, 0, lambda x, y: map[y][x] + 1)

def part_2(map):
    basin_sizes = apply_to_lowest(map, [], lambda x, y, map = map: [Bfs(map, start = (x, y))])
    basin_sizes.sort(reverse = True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


with open('../input/day9.txt') as istream:
    map = [[int(n) for n in line.rstrip('\n')] for line in istream.readlines()]
    print('Part 1: ', part_1(map.copy()))    
    print('Part 2: ', part_2(map.copy()))    

