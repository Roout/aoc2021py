import time
import re

class Vec2:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return '[{}, {}]'.format(self.x, self.y)

    def __repr__(self) -> str:
        return self.__str__()
    
class Rect:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x, y) -> bool:
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height
    
    def __str__(self) -> str:
        return '[x = {}, y = {}, w = {}, h = {}]'.format(self.x, self.y, self.width, self.height)

    def __repr__(self) -> str:
        return self.__str__()
    
# Due to drag, the probe's x velocity changes by 1 toward the value 0; 
#       that is, it decreases by 1 if it is greater than 0, 
#       increases by 1 if it is less than 0, or does not change if it is already 0.
# Due to gravity, the probe's y velocity decreases by 1.
def update(vel: Vec2):
    if vel.x != 0:
        vel.x += -1 if vel.x > 0 else 1  
    vel.y -= 1

def simulator(start: Vec2, vel: Vec2):
    cur = start
    while True:
        cur.x += vel.x
        cur.y += vel.y
        yield cur
        update(vel)

def part_1(target: Rect):
    limiter_x = target.x + target.width
    limiter_y = target.y - 1

    for y in reversed(range(0, -2 * limiter_y)):
        for x in range(1, limiter_x):
            mx = 0
            gen = simulator(Vec2(0, 0), Vec2(x, y))
            for i__ in range(800):
                pos = next(gen)
                if pos.x >= limiter_x or pos.y <= limiter_y:
                    # won't reach the target area for sure
                    break
                mx = pos.y if mx < pos.y else mx
                if target.contains(pos.x, pos.y):
                    return mx
    return None

def part_2(target: Rect):
    limiter_x = target.x + target.width
    limiter_y = target.y - 1

    velocities = 0
    # choose range taking into account negative values too
    # because this time we are interesting in not the best but any velocity
    for y in reversed(range(limiter_y, -2 * limiter_y)):
        for x in range(1, limiter_x):
            is_valid = False
            gen = simulator(Vec2(0, 0), Vec2(x, y))
            for i__ in range(800):
                pos = next(gen)
                if pos.x >= limiter_x or pos.y <= limiter_y:
                    # won't reach the target area for sure
                    break
                if target.contains(pos.x, pos.y):
                    is_valid = True
                    break
            velocities += int(is_valid)
                    
    return velocities

target = None
with open("../input/day17.txt") as istream:
    result = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', istream.readline())
    x0 = int(result.group(1))
    x1 = int(result.group(2))
    y0 = int(result.group(3))
    y1 = int(result.group(4))
    target = Rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1)
    
begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(target), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(target), time.time() - begin))
