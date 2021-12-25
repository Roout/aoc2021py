import time
from typing import Dict, List, Set, Tuple

class Amphipod:
    
    def __init__(self, name: str, pos: Tuple) -> None:
        self.name = name
        self.pos = pos
        cost = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }
        self.cost = cost[name]

    def __str__(self) -> str:
        return '{} at {}'.format(self.name, self.pos)
    
    def __repr__(self) -> str:
        return self.__str__()

    def move(self, pos: Tuple):
        self.pos = pos

class Map:

    def __init__(self, map: List[str]) -> None:
        self.score = 30000
        self.map = map
        self.amphipods = []
        self.rooms = {
            'A': [(3,2), (3,3)],
            'B': [(5,2), (5,3)],
            'C': [(7,2), (7,3)],
            'D': [(9,2), (9,3)]}
        self.entrance = [(3,1), (5,1), (7,1), (9,1)]
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y][x] != '.' and map[y][x] != '#':
                    self.amphipods.append(Amphipod(map[y][x], (x, y)))
                

    @staticmethod
    def manh(src: tuple, dst: tuple):
        return abs(src[0] - dst[0]) + abs(src[1] - dst[1])

    def completed(self):
        for amph in self.amphipods:
            if amph.pos not in self.rooms[amph.name]:
                return False
        return True

    def occupied_by(self, pos: Tuple):
        if self.map[pos[1]][pos[0]] == '#':
            return None
        for amph in self.amphipods:
            if amph.pos == pos:
                return amph
        return None
        
    def dfs(self, src: tuple, dst: tuple):
        shifts = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        vis = set()
        vis.add(src)
        que = [(src, 0)]
        while len(que) > 0:
            front, length = que.pop(0)
            if front == dst:
                return length
            for sh in shifts:
                next = (sh[0] + front[0], sh[1] + front[1])
                if (self.map[next[1]][next[0]] != '#' and 
                    next not in vis and 
                    self.occupied_by(next) == None
                ):
                    vis.add(next)
                    que.append((next, length + 1))
        return None


    def allowed_moves(self, amph: Amphipod):
        allowed: List[Tuple] = []
        rooms = self.rooms[amph.name]
        rooms_count = len(rooms)
        assert rooms_count == 2
        
        if amph.pos[1] != 1: # in room
            # if already in needed room
            if rooms[1] == amph.pos:
                # already in the farthest room, no more moves make sense
                return []
            # check near-entrance room
            if rooms[0] == amph.pos:
                other = self.occupied_by(rooms[1])
                if other != None and other.name == amph.name:
                    # have same type of amph as a neighbour
                    return []
            # otherwise add to hall
            for x in range(1, len(self.map[0]) - 1):
                dst = (x, 1)
                if dst not in self.entrance:
                    length = self.dfs(amph.pos, dst)
                    if length is not None:
                        allowed.append((dst, length))

        # in hall
        if self.occupied_by(rooms[0]) is not None:
            # whatever it is we can't move through it 
            return allowed
        
        other = self.occupied_by(rooms[1])
        if other is None:
            for i in range(2):
                length = self.dfs(amph.pos, rooms[i])
                if length != None:
                    allowed.append((rooms[i], length))
        elif other.name == amph.name:
            length = self.dfs(amph.pos, rooms[0])
            if length != None:
                allowed.append((rooms[0], length))
        return allowed

    def simulate(self, moved: Dict[Amphipod, int], score: int):
        if score >= self.score:
            return

        if self.completed():
            self.score = score
            print(self.score)
            return

        for amph in self.amphipods:
            if moved[amph] >= 2:
                continue
            src = amph.pos
            allowed = self.allowed_moves(amph)
            if len(allowed) == 0:
                continue
            # print('{} at {}'.format(amph.name, amph.pos))
            for dst, length in allowed:
                # print('  -> from {} to {}'.format(amph.pos, dst))
                amph.move(dst)
                moved[amph] += 1
                self.simulate(moved, score + length * amph.cost)
                moved[amph] -= 1
                amph.move(src)

def part_1(raw):
    map = Map(raw)
    moved = {}
    for amph in map.amphipods:
        moved[amph] = 0
    map.simulate(moved, 0)
    return map.score

def part_2(raw):
    pass

raw = []
with open("../input/day23.txt") as istream:
    for line in istream:
        raw.append(line.rstrip())
    
begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(raw), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(raw), time.time() - begin))
