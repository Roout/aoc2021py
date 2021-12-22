import time
import itertools
from typing import List

class Player:
    def __init__(self, pos: int) -> None:
        self.position = pos
        self.score = 0

    def move(self, delta: int):
        self.position = (self.position + delta - 1) % 10 + 1
        self.score += self.position
    
    def win(self):
        return self.score >= 1000

def rolls():
    cur = 1
    while True:
        sum = 0
        for i in range(3):
            sum += cur
            cur = cur % 100 + 1
        yield sum
        
def part_1(pos: List):
    players = [ Player(pos[0]), Player(pos[1]) ]
    die = rolls()
    nrolls = 0
    while True:
        players[0].move(next(die))
        nrolls += 3
        if players[0].win(): break

        players[1].move(next(die))
        nrolls += 3
        if players[1].win(): break

    loser = players[0].score if players[0].score < players[1].score else players[1].score
    return nrolls * loser

def all_dices():
    counter = {}
    for seq in itertools.product([1,2,3], repeat = 3):
        sum = 0
        for x in seq: 
            sum += x
        if sum in counter:
            counter[sum] += 1
        else:
            counter[sum] = 1
    return counter

def solve(turn, scores, pos, cache, dices):
    # check cached
    state = tuple(pos + scores + [turn])
    if state in cache:
        return cache[state]

    if scores[0] >= 21:
        cache[state] = [1, 0]
        return [1, 0]

    if scores[1] >= 21:
        cache[state] = [0, 1]
        return [0, 1]
   
    wins = [0, 0]
    for dice, count in dices.items():
        npos = pos.copy()
        nscores = scores.copy()
        npos[turn] = (pos[turn] + dice - 1) % 10 + 1
        nscores[turn] += npos[turn]

        res = solve(turn ^ 1, nscores, npos, cache, dices)

        wins[0] += res[0] * count
        wins[1] += res[1] * count

    # assert state not in cache
    cache[state] = wins

    return wins

def part_2(pos: List):
    cache = {}
    dices = all_dices()
    wins = solve(0, [0, 0], pos.copy(), cache, dices)
    return max(wins)

pos = [0, 0]
with open("../input/day21.txt") as istream:
    pos[0] = int(istream.readline().rstrip().split(':')[1])
    pos[1] = int(istream.readline().rstrip().split(':')[1])
    
begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(pos), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(pos), time.time() - begin))
