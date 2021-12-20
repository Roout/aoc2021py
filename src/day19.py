import time
import re
import itertools
from typing import Iterable, List

class Point:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return '{{{},{},{}}}'.format(self.x, self.y, self.z)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, rhs: "Point") -> bool:
        return self.x == rhs.x and self.y == rhs.y and self.z == rhs.z
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def copy(self):
        return Point(self.x, self.y, self.z)

    def shuffle(self, order: str):
        copy = [self.x, self.y, self.z]
        for i in range(len(order)):
            if order[i] == 'x':
                self.x = copy[i]
            elif order[i] == 'y':
                self.y = copy[i]
            elif order[i] == 'z':
                self.z = copy[i]
            else:
                assert False, 'Unreachable'

    @classmethod
    def from_list(cls, conf: List[int]):
        return cls(conf[0], conf[1], conf[2])

def mul(lhs: Point, rhs: Point):
    return Point(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z)

def sub(lhs: Point, rhs: Point):
    return Point(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z)

def add(lhs: Point, rhs: Point):
    return Point(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z)

def neg(lhs: Point):
    return Point(-lhs.x, -lhs.y, -lhs.z)

def cross(lhs: Point, rhs: Point):
    return Point(lhs.y * rhs.z - lhs.z * rhs.y,
        lhs.z * rhs.x - lhs.x * rhs.z,
        lhs.x * rhs.y - lhs.y * rhs.x)
    
def dot(lhs: Point, rhs: Point):
    return lhs.x * rhs.x + lhs.y * rhs.y + lhs.z * rhs.z

def manh_dist(lhs: Point, rhs: Point):
    return abs(lhs.x - rhs.x) + abs(lhs.y - rhs.y) + abs(lhs.z - rhs.z)

# transform is a list/tuple of valid right-handed permutation of [1,2,3]
# with possible different signs
# see `generate_trans()``
def rotate(point: Point, transform: Iterable):
    assert isinstance(transform, list) or isinstance(transform, tuple)
    vec = (point.x, point.y, point.z)
    return Point(vec[abs(transform[0]) - 1] * (1 if transform[0] > 0 else -1),
            vec[abs(transform[1]) - 1] * (1 if transform[1] > 0 else -1),
            vec[abs(transform[2]) - 1] * (1 if transform[2] > 0 else -1))

def generate_trans():
    rotations = [[1, 1, 1], [1, 1, -1], [1, -1, 1], 
        [1, -1, -1], [-1, 1, 1], [-1, 1, -1], 
        [-1, -1, 1], [-1, -1, -1]]
    orders = [''.join(x) for x in itertools.permutations('123')]
    transformations = [[int(r[i]) if l[i] == 1 else int('-' + r[i]) for i in range(len(r))] for (l, r) in itertools.product(rotations, orders)]
    # return list(filter(is_right_handed, transformations))
    return transformations

class Scanner:
    def __init__(self, index: int) -> None:
        self.points = list()
        self.index = index
        self.position = None

    def __str__(self) -> str:
        return 'index: {} at: {} points: {}'.format(self.index, self.position, self.points)

    def __repr__(self) -> str:
        return self.__str__()

    def rotate(self, transform: Iterable):
        for i, p in enumerate(self.points):
            self.points[i] = rotate(p, transform)
        return self

    def translate(self, vec: Point):
        for i in range(len(self.points)):
            self.points[i] = add(self.points[i], vec)
        return self

    def copy(self):
        scanner = Scanner(self.index)
        scanner.points = self.points[:]
        scanner.position = self.position
        return scanner

    def in_range(self, point: Point) -> bool:
        return (abs(self.position.x - point.x) <= 1000 
            and abs(self.position.y - point.y) <= 1000 
            and abs(self.position.z - point.z) <= 1000)

def is_right_handed(transform: Iterable):
    assert isinstance(transform, list) or isinstance(transform, tuple)
    a = Point(transform[0], 0, 0)
    b = Point(0, transform[1], 0)
    c = Point(0, 0, transform[2])
    return dot(cross(a, b), c) >= 0

def intersect(lhs:Scanner, rhs:Scanner):
    assert lhs != rhs
    coincide = [p for p in lhs.points if p in rhs.points]
    return coincide

def all_translations(src:Scanner, dst:Scanner):
    translations = [sub(p2, p1) for p1 in src.points for p2 in dst.points]
    return translations

def configure_scanners(scanners: List[Scanner]):
    REQ_BEACONS = 12
    proccessed = []
    transformations = generate_trans()
    scanners[0].position = Point(0, 0, 0)
    que = [scanners.pop(0)]

    while len(que) > 0:
        front = que.pop(0)
        proccessed += [front]
        scheduled_for_remove = []
        for scanner in scanners:
            print('Test s{} with s{}'.format(front.index, scanner.index))
            # for each possible configuration of the `scanner``
            for transform in transformations:
                found = False
                # rotate
                rotated = scanner.copy().rotate(transform)
                assert len(rotated.points) == len(scanner.points)
                
                # check each possible translate
                translations = all_translations(front, rotated)        
                assert len(translations) == len(front.points) * len(rotated.points)
                
                for v in translations:
                    translated = rotated.copy().translate(neg(v))
                    coincided = intersect(front, translated)
                    if len(coincided) >= REQ_BEACONS:
                        translated.position = neg(v)
                        que += [translated]
                        scheduled_for_remove += [scanner]
                        print('  s{} overlap with s{} which is at position {}'.format(front.index, translated.index, neg(v)))
                        found = True
                        break
                if found: break
        if len(scheduled_for_remove) > 0:
            # print('  scheduled_for_remove:', len(scheduled_for_remove))
            scanners[:] = (x for x in scanners if (x not in scheduled_for_remove))
    return proccessed

def part_1(scanners: List[Scanner]):
    proccessed = configure_scanners(scanners)
    beacons = set()
    points = set()
    for scan in proccessed:
        points.update(scan.points)
    for scan in proccessed:
        for point in points:
            if scan.in_range(point):
                beacons.add(point)
    return len(beacons)

def part_2(scanners: List[Scanner]):
    proccessed = configure_scanners(scanners)
    longest = 0
    for s1 in proccessed:
        for s2 in proccessed:
            if s1 == s2: continue
            d = manh_dist(s1.position, s2.position)
            if d > longest:
                longest = d
    return longest

scanners: List[Scanner] = list()
with open("../input/day19.txt") as istream:
    for line in istream:
        line = line.rstrip()
        if len(line) == 0:
            continue
        m = re.match(r'--- scanner (\d+) ---', line)
        if m != None:
            scanners += [Scanner(int(m.group(1)))]
        else:
            x, y, z = line.split(',')        
            scanners[-1].points += [ Point(int(x), int(y), int(z)) ]

begin = time.time()
# print('Part_1: {}, takes {}s'.format(part_1([s.copy() for s in scanners]), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2([s.copy() for s in scanners]), time.time() - begin))
