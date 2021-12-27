import abc
from dataclasses import dataclass, field
from heapq import heappop, heappush
import time
from typing import Dict, List, Set, Tuple

def assign_or_modify(d: dict, key, value):
    if key not in d:
        d[key] = value
    else:
        d[key] += value

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

@dataclass(order = True)
class Move:
    score: int
    state: State = field(compare = False)

class Map(metaclass = abc.ABCMeta):
    SHIFTS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    ENTRANCE = [(3,1), (5,1), (7,1), (9,1)]

    def __init__(self, map: List[str]) -> None:
        self.map = map
        self.rooms: Dict[str, List[Tuple]] = self._define_rooms()
        self.initial_state: State = self._define_initial_state()
        self.final_state: State = self._define_final_state()

    def _define_initial_state(self):
        amphipods = []
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] != '.' and self.map[y][x] != '#':
                    amphipods.append(Amphipod(self.map[y][x], (x, y)))
        return State(amphipods)

    def _define_final_state(self) -> State:
        dst = []
        for key, values in self.rooms.items():
            for v in values:
                dst.append(Amphipod(key, v))
        return State(dst)

    @abc.abstractmethod
    def _define_rooms(self) -> Dict[str, List[Tuple]]:
        pass
    
    @abc.abstractmethod
    def allowed_moves(self, amph: Amphipod, state: State) -> List[Tuple]:
        pass


    def is_final(self, state: State) -> bool:
        return state.hash == self.final_state.hash
    
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
        
    def distance(self, src: tuple, dst: tuple, state: State):
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
            
            if self.is_final(state):
                return score

            for amph in state.amphipods:
                if amph.moved >= 2:
                    continue
                for (length, dst) in self.allowed_moves(amph, state):
                    cost = length * amph.cost
                    next_state = state.get_next(amph, dst)
                    if (next_state.hash not in vis 
                        or vis[next_state.hash] > score + cost
                    ):
                        assign_or_modify(vis, next_state.hash, score + cost)
                        heappush(opened, Move(score + cost, next_state))
        return None
    
class MapPart_1(Map):

    def _define_rooms(self) -> Dict[str, List[Tuple]]:
        rooms = {
            'A': [(3,2), (3,3)],
            'B': [(5,2), (5,3)],
            'C': [(7,2), (7,3)],
            'D': [(9,2), (9,3)] }
        return rooms
    
    def allowed_moves(self, amph: Amphipod, state: State) -> List[Tuple]:
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
                if dst not in Map.ENTRANCE:
                    length = self.distance(amph.pos, dst, state)
                    if length is not None:
                        allowed.append((length, dst))

        # in hall
        if self.occupied_by(rooms[0], state) is not None:
            # whatever it is we can't move through it 
            return allowed
        
        other = self.occupied_by(rooms[1], state)
        if other is None:
            for i in range(2):
                length = self.distance(amph.pos, rooms[i], state)
                if length != None:
                    allowed.append((length, rooms[i]))
        elif other.name == amph.name:
            length = self.distance(amph.pos, rooms[0], state)
            if length != None:
                allowed.append((length, rooms[0]))
        return allowed

class MapPart_2(Map):

    def _define_rooms(self) -> Dict[str, List[Tuple]]:
        rooms = {
            'A': [(3,2), (3,3), (3,4), (3,5)],
            'B': [(5,2), (5,3), (5,4), (5,5)],
            'C': [(7,2), (7,3), (7,4), (7,5)],
            'D': [(9,2), (9,3), (9,4), (9,5)] }
        return rooms

    def allowed_moves(self, amph: Amphipod, state: State) -> List[Tuple]:
        allowed: List[Tuple] = []
        rooms = self.rooms[amph.name]
        rooms_count = len(rooms)
        assert rooms_count == 4

        if amph.pos[1] != 1: 
            # in room
            # do I even need to move? 
            at_room = None
            for i in range(rooms_count):
                if rooms[i] == amph.pos:
                    at_room = i
                    break
            if at_room != None:
                # already at one of possible destination
                need_to_move = False
                for i in range(at_room + 1, rooms_count):
                    occupant = self.occupied_by(rooms[i], state) 
                    if occupant == None or occupant.name != amph.name:
                        need_to_move = True
                        break
                if need_to_move == False:
                    # no need to move, already at it's place
                    return allowed
            # otherwise add to hall
            for x in range(1, len(self.map[0]) - 1):
                dst = (x, 1)
                if dst not in Map.ENTRANCE:
                    length = self.distance(amph.pos, dst, state)
                    if length is not None:
                        allowed.append((length, dst))
        else:
            # from hall to room
            length = self.distance(amph.pos, rooms[0], state)
            if length == None:
                # can't reach room
                return []
            first_occupied_room_index = None
            for i in range(1, rooms_count):
                occupant = self.occupied_by(rooms[i], state)
                if occupant != None and occupant.name != amph.name:
                    return []
                if occupant != None:
                    first_occupied_room_index = i
                    break
            if first_occupied_room_index != None:
                # confirm that there is no other occupant with other name 
                # or free space
                for i in range(first_occupied_room_index + 1, rooms_count):
                    occupant = self.occupied_by(rooms[i], state)
                    if occupant == None or occupant.name != amph.name:
                        return []
            else:
                first_occupied_room_index = rooms_count
            # add empty rooms
            for i in range(first_occupied_room_index):
                allowed.append((length + i, rooms[i]))
        return allowed

def part_1(raw):
    # convert part 2 input to part 1 inpot
    map: List[str] = []
    for i in range(len(raw)):
        if i == 3 or i == 4:
            continue
        map.append(raw[i])
    return MapPart_1(map).search()

def part_2(raw):
    return MapPart_2(raw).search()

raw = []
with open("../input/day23.txt") as istream:
    for line in istream:
        raw.append(line.rstrip())
    
begin = time.time()
# takes 280.8341495990753s
print('Part_1: {}, takes {}s'.format(part_1(raw), time.time() - begin))
begin = time.time()
# takes 141.15754175186157s
print('Part_2: {}, takes {}s'.format(part_2(raw), time.time() - begin))
