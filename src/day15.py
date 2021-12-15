from heapq import *
from dataclasses import dataclass, field
from typing import Any

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

    def __init__(self, prior: int, pos: Pt) -> None:
        self.priority = prior
        self.item = pos
        

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
    return dijkstra(map, Pt(0,0), Pt(len(map[0]) - 1, len(map) - 1))

map = []
with open('../input/day15.txt') as istream:
    for line in istream:
        map += [[int(x) for x in line.rstrip('\n')]]

print('Part_1: ', part_1(map))
