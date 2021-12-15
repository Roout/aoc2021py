from heapq import *
from dataclasses import dataclass, field
import time

class Pt:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, rhs: object) -> bool:
        return self.x == rhs.x and self.y == rhs.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

@dataclass(order=True)
class Move:
    priority: int
    item: Pt = field(compare=False)

def add(lhs: Pt, rhs: Pt):
    return Pt(lhs.x + rhs.x, lhs.y + rhs.y)

def is_valid(map: list, pos: Pt):
    return 0 <= pos.x < len(map[0]) and 0 <= pos.y < len(map)

def assign_or_modify(d: dict, key, value):
    if key not in d:
        d[key] = value
    else:
        d[key] += value

def dijkstra(map: list, start: Pt, finish:Pt):
    shifts = [Pt(-1, 0), Pt(1, 0), Pt(0, -1), Pt(0, 1)]

    used = [[False] * len(row) for row in map]
    cur_risks = dict()
    queue = []
    heappush(queue, Move(0, start))

    while len(queue) > 0:
        top = heappop(queue)
        cave = top.item
        risk = top.priority
        used[cave.y][cave.x] = True
        if cave == finish:
            return risk
        for move in shifts:
            to = add(cave, move)
            if is_valid(map, to) and used[to.y][to.x] == False:
                move_risk = map[to.y][to.x] + risk
                if to not in cur_risks or cur_risks[to] > move_risk:
                    assign_or_modify(cur_risks, to, move_risk)
                    heappush(queue, Move(move_risk, to))
    # no path exist
    return None

def part_1(map: list):
    return dijkstra(map, Pt(0, 0), Pt(len(map[0]) - 1, len(map) - 1))

def part_2(map: list):
    h = len(map)
    enlarged_map = [[] for r in range(5 * h)]

    for i in range(h):
        for j in range(5):
            enlarged_map[i] += [(val + j - 1) % 9 + 1 for val in map[i]]
    
    for i in range(1, 5):
        for j in range(h):
            enlarged_map[i * h + j] = [(val + i - 1) % 9 + 1 for val in enlarged_map[j]]

    return dijkstra(enlarged_map, Pt(0, 0), Pt(len(enlarged_map[0]) - 1, len(enlarged_map) - 1))

map = []
with open('../input/day15.txt') as istream:
    for line in istream:
        map += [[int(x) for x in line.rstrip('\n')]]

begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(map), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(map), time.time() - begin))
