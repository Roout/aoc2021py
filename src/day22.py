import time
from typing import List

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

    @classmethod
    def from_list(cls, conf: List[int]):
        return cls(conf[0], conf[1], conf[2])

def sub(lhs: Point, rhs: Point):
    return Point(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z)

def add(lhs: Point, rhs: Point):
    return Point(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z)

class Cube:
    def __init__(self, p: Point, size: Point) -> None:
        self.pos = p.copy()
        self.size = size.copy()

    def __str__(self) -> str:
        return '[p: {}, sz: {}]'.format(self.pos, self.size)

    def __repr__(self) -> str:
        return self.__str__()

    def volume(self) -> int:
        return self.size.x * self.size.y * self.size.z
    
    def same(self, cube: 'Cube'):
        return self.pos == cube.pos and self.size == cube.size

    def split(self, cube: 'Cube'):
        """"@cube must be result of intersect: must be inside this `self` cube"""
        cubes = []
        # slice up-z
        if cube.pos.z + cube.size.z < self.pos.z + self.size.z:
            up_z_cube = Cube(
                Point(self.pos.x, self.pos.y, cube.pos.z + cube.size.z),
                Point(self.size.x, self.size.y, self.pos.z + self.size.z - cube.pos.z - cube.size.z))
            cubes += [up_z_cube]
        # slice down-z
        if cube.pos.z > self.pos.z:
            down_z_cube = Cube(
                Point(self.pos.x, self.pos.y, self.pos.z),
                Point(self.size.x, self.size.y, cube.pos.z - self.pos.z))
            cubes += [down_z_cube]
        # slice back-y
        if cube.pos.y + cube.size.y < self.pos.y + self.size.y:
            back_y_cube = Cube(
                Point(self.pos.x, cube.pos.y + cube.size.y, cube.pos.z),
                Point(self.size.x, self.pos.y + self.size.y - cube.pos.y - cube.size.y, cube.size.z))
            cubes += [back_y_cube]
        # slice front-y
        if cube.pos.y > self.pos.y:
            front_y_cube = Cube(
                Point(self.pos.x, self.pos.y, cube.pos.z),
                Point(self.size.x, cube.pos.y - self.pos.y, cube.size.z))
            cubes += [front_y_cube]
        # slice right-x
        if cube.pos.x + cube.size.x < self.pos.x + self.size.x:
            right_x_cube = Cube(
                Point(cube.pos.x + cube.size.x, cube.pos.y, cube.pos.z),
                Point(self.pos.x + self.size.x - cube.pos.x - cube.size.x, cube.size.y, cube.size.z))
            cubes += [right_x_cube]
        # slice left-x
        if cube.pos.x > self.pos.x:
            left_x_cube = Cube(
                Point(self.pos.x, cube.pos.y, cube.pos.z),
                Point(cube.pos.x - self.pos.x, cube.size.y, cube.size.z))
            cubes += [left_x_cube]
        return cubes

    def intersect(self, rhs: 'Cube'):
        mn_x = self if self.pos.x <= rhs.pos.x else rhs
        mx_x = self if self.pos.x >  rhs.pos.x else rhs
        assert mn_x != mx_x
        if mn_x.pos.x + mn_x.size.x <= mx_x.pos.x:
            return None

        mn_y = self if self.pos.y <= rhs.pos.y else rhs
        mx_y = self if self.pos.y >  rhs.pos.y else rhs
        assert mn_y != mx_y
        if mn_y.pos.y + mn_y.size.y <= mx_y.pos.y:
            return None

        mn_z = self if self.pos.z <= rhs.pos.z else rhs
        mx_z = self if self.pos.z >  rhs.pos.z else rhs
        assert mn_z != mx_z
        if mn_z.pos.z + mn_z.size.z <= mx_z.pos.z:
            return None

        res_pos = Point(mx_x.pos.x, mx_y.pos.y, mx_z.pos.z) 
        res_size = Point(
            min(mn_x.pos.x + mn_x.size.x - mx_x.pos.x, mx_x.size.x),
            min(mn_y.pos.y + mn_y.size.y - mx_y.pos.y, mx_y.size.y),
            min(mn_z.pos.z + mn_z.size.z - mx_z.pos.z, mx_z.size.z)) 

        return Cube(res_pos, res_size)    

def add_lit(lit: List[Cube], cube: Cube):
    other = [cube]
    while len(other) > 0:
        front = other.pop(0)
        
        new_parts = []
        schedule_for_remove = None
        schedule_for_work = []
        for lit_cube in lit:
            intersection = lit_cube.intersect(front)
            if intersection != None:
                new_parts.append(intersection)
                new_parts += lit_cube.split(intersection)
                schedule_for_remove = lit_cube
                schedule_for_work = front.split(intersection)   
                break

        if schedule_for_remove == None:
            lit.append(front)
        else:
            lit.remove(schedule_for_remove)
            lit += new_parts
            other += schedule_for_work
        
    return lit

def add_off(lit: List[Cube], off: Cube):
    other = [off]
    # while all `off` cubes not handled!
    while len(other) > 0:
        front = other.pop(0)
        new_parts = []
        schedule_for_remove = None
        schedule_for_work = []
        for lit_cube in lit:
            intersection = lit_cube.intersect(front)
            if intersection != None:
                # print('intersection:', lit_cube, 'with', front)
                # print('turn off:', intersection, 'with valume:', intersection.volume())
                # for x in range(intersection.pos.x, intersection.pos.x + intersection.size.x):
                #     for y in range(intersection.pos.y, intersection.pos.y + intersection.size.y):
                #         for z in range(intersection.pos.z, intersection.pos.z + intersection.size.z):
                #             print('  >', x, y, z)
                new_parts += lit_cube.split(intersection)
                # print('new on parts:', lit_cube.split(intersection))
                schedule_for_remove = lit_cube
                schedule_for_work = front.split(intersection)   
                # print('new off parts:', schedule_for_work)
                break

        if schedule_for_remove != None:
            lit.remove(schedule_for_remove)
            lit += new_parts
            other += schedule_for_work

    return lit

def part_1(actions: List[str], cubes: List[Cube]):
    lit = [cubes.pop(0)]
    actions.pop(0)

    bounds = Cube(Point(-50,-50,-50), Point(101,101,101))

    for cube in cubes:
        a = actions.pop(0)
        intersection = bounds.intersect(cube)
        # print(intersection)
        if intersection == None: 
            continue
        if a == 'on':
            lit = add_lit(lit, intersection)
        else:
            lit = add_off(lit, intersection)
    # print(lit)
    s = 0
    for x in lit:
        s += x.volume()
    return s    

def part_2(actions: List[str], cubes: List[Cube]):
    pass

cubes: List[Cube] = []
actions: List[str] = []
with open("../input/day22.txt") as istream:
    for line in istream:
        splited = line.rstrip().split('=')
        actions += [splited[0].split(' ')[0]]
        splited = splited[1:]
        a = Point(
            int(splited[0].split('..')[0]),
            int(splited[1].split('..')[0]),
            int(splited[2].split('..')[0]),
        )
        b = Point(
            int(splited[0].split('..')[1].removesuffix(',y')),
            int(splited[1].split('..')[1].removesuffix(',z')),
            int(splited[2].split('..')[1]),
        )
        cubes += [Cube(a, add(sub(b, a), Point(1, 1, 1)))]
    
begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(actions, cubes), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(actions, cubes), time.time() - begin))
