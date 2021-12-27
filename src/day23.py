from dataclasses import dataclass, field
from heapq import heappop, heappush
import time
from typing import Dict, List, Set, Tuple

class Amphipod:
    cost = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }
    
    def __init__(self, name: str, pos: Tuple, moved: int = 0) -> None:
        self.name = name
        self.pos = pos
        self.cost = Amphipod.cost[name]
        self.moved = moved

    def __str__(self) -> str:
        return '{} at {}'.format(self.name, self.pos)
    
    def __eq__(self, amph: "Amphipod") -> bool:
        if amph == None:
            return False
        return amph.name == self.name and amph.pos == self.pos

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.name, self.pos[0], self.pos[1]))

    def copy(self):
        return Amphipod(self.name, self.pos, self.moved)

    def move(self, pos: Tuple):
        self.pos = pos
        self.moved += 1

class State:
    def __init__(self, amphipods: List[Amphipod]) -> None:
        self.amphipods = [x.copy() for x in amphipods]
        self.amphipods.sort(key = lambda amph: (amph.name, amph.pos[0], amph.pos[1]))
        self.hash = hash(tuple(self.amphipods))

    def __eq__(self, __o: "State") -> bool:
        return __o.hash == self.hash

    def __hash__(self) -> int:
        return self.hash

    def get_next(self, amphipod: Amphipod, pos: Tuple):
        amphipods = [x.copy() for x in self.amphipods]
        for x in amphipods:
            if amphipod == x:
                x.move(pos)
                break
        return State(amphipods)

def assign_or_modify(d: dict, key, value):
    if key not in d:
        d[key] = value
    else:
        d[key] += value

@dataclass(order = True)
class Move:
    score: int
    state: State = field(compare=False)


class Map:
    SHIFTS = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def __init__(self, map: List[str]) -> None:
        self.score = 30000
        self.map = map
        self.rooms = {
            'A': [(3,2), (3,3)],
            'B': [(5,2), (5,3)],
            'C': [(7,2), (7,3)],
            'D': [(9,2), (9,3)]}

        dst_1 = []
        for key, values in self.rooms.items():
            for v in values:
                dst_1.append(Amphipod(key, v))
        self.final_1 = State(dst_1)
        self.entrance = [(3,1), (5,1), (7,1), (9,1)]
        amphipods = []
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y][x] != '.' and map[y][x] != '#':
                    amphipods.append(Amphipod(map[y][x], (x, y)))
        self.initial_state = State(amphipods)
                
    def completed_1(self, state: State):
        return state.hash == self.final_1.hash

    def occupied_by(self, pos: Tuple, state: State):
        if self.map[pos[1]][pos[0]] == '#':
            return None
        for amph in state.amphipods:
            if amph.pos == pos:
                return amph
        return None
    
    def dump_state(self, state: State):
        img = []
        for row in self.map:
            img.append([])
            for col in row:
                img[-1].append(col if col == '.' or col == '#' else '.')
        for amph in state.amphipods:
            img[amph.pos[1]][amph.pos[0]] = amph.name[0]
        for row in img:
            print(''.join(row))


    def dfs(self, src: tuple, dst: tuple, state: State):
        vis = set()
        vis.add(src)
        que = [(src, 0)]
        while len(que) > 0:
            front, length = que.pop(0)
            if front == dst:
                return length
            for sh in Map.SHIFTS:
                next = (sh[0] + front[0], sh[1] + front[1])
                if (self.map[next[1]][next[0]] != '#' and 
                    next not in vis and 
                    self.occupied_by(next, state) == None
                ):
                    vis.add(next)
                    que.append((next, length + 1))
        return None


    def allowed_moves(self, amph: Amphipod, state: State):
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
                other = self.occupied_by(rooms[1], state)
                if other != None and other.name == amph.name:
                    # have same type of amph as a neighbour
                    return []
            # otherwise add to hall
            for x in range(1, len(self.map[0]) - 1):
                dst = (x, 1)
                if dst not in self.entrance:
                    length = self.dfs(amph.pos, dst, state)
                    if length is not None:
                        allowed.append((length, dst))

        # in hall
        if self.occupied_by(rooms[0], state) is not None:
            # whatever it is we can't move through it 
            return allowed
        
        other = self.occupied_by(rooms[1], state)
        if other is None:
            for i in range(2):
                length = self.dfs(amph.pos, rooms[i], state)
                if length != None:
                    allowed.append((length, rooms[i]))
        elif other.name == amph.name:
            length = self.dfs(amph.pos, rooms[0], state)
            if length != None:
                allowed.append((length, rooms[0]))
        return allowed

    def search(self):
        opened = []
        initial = self.initial_state
        heappush(opened, Move(0, initial))
        vis = {
            initial.hash: 0 # state - score
        }

        while len(opened) > 0:
            top = heappop(opened)
            score = top.score
            state = top.state
            if len(opened) % 30000 == 0:
                print(len(vis), len(opened), score)
                self.dump_state(state)
            
            if self.completed_1(state):
                return score

            for amph in state.amphipods:
                if amph.moved >= 2:
                    continue
                for (length, dst) in self.allowed_moves(amph, state):
                    cost = length * amph.cost
                    if score + cost > 18500:
                        continue
                    next_state = state.get_next(amph, dst)
                    if (next_state.hash not in vis 
                        or vis[next_state.hash] > score + cost
                    ):
                        assign_or_modify(vis, next_state.hash, score + cost)
                        heappush(opened, Move(score + cost, next_state))
        return None

def part_1(raw):
    map = Map(raw)
    return map.search()

def part_2(raw):
    pass

raw = []
with open("../input/day23.txt") as istream:
    for line in istream:
        raw.append(line.rstrip())
    
begin = time.time()
# takes 280.8341495990753s
print('Part_1: {}, takes {}s'.format(part_1(raw), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(raw), time.time() - begin))
