import re

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __repr__(self) -> str:
        return '(' + str(self.x1) + ',' + str(self.y1) + ') -> (' + str(self.x2) + ',' + str(self.y2) + ')'

    def __str__(self) -> str:
        return self.__repr__()

def part_1(segments):
    size = 1000
    crossed = [[0 for t in range(size)] for tt in range(size)]
    for s in segments:
        # print(s)
        if s.x1 == s.x2:
            mn = min(s.y1, s.y2)
            mx = max(s.y1, s.y2)
            for y in range(mn, mx + 1):
                crossed[y][s.x1] += 1
        elif s.y1 == s.y2:
            mn = min(s.x1, s.x2)
            mx = max(s.x1, s.x2)
            for x in range(mn, mx + 1):
                crossed[s.y1][x] += 1
        # for row in crossed:
        #     print(row)
        # print('---------------')
    count = 0
    for row in crossed:
        for v in row:
            count += (v > 1)
    # for row in crossed:
    #     print(row)
    return count

def part_2(segments):
    size = 1000
    crossed = [[0 for t in range(size)] for tt in range(size)]
    for s in segments:
        # print(s)
        if s.x1 == s.x2:
            mn = min(s.y1, s.y2)
            mx = max(s.y1, s.y2)
            for y in range(mn, mx + 1):
                crossed[y][s.x1] += 1
        elif s.y1 == s.y2:
            mn = min(s.x1, s.x2)
            mx = max(s.x1, s.x2)
            for x in range(mn, mx + 1):
                crossed[s.y1][x] += 1
        else:
            # src
            x1, y1 = s.x1, s.y1
            # dst
            x2, y2 = s.x2, s.y2
            # move and mark
            while x1 != x2 and y1 != y2:
                crossed[y1][x1] += 1
                if x1 != x2:
                    x1 += 1 if x1 < x2 else -1
                if y1 != y2:
                    y1 += 1 if y1 < y2 else -1
            crossed[y1][x1] += 1
        # for row in crossed:
        #     print(row)
        # print('---------------')
    count = 0
    for row in crossed:
        for v in row:
            count += (v > 1)
    return count

segments = []
with open('../input/day5.txt', 'r') as istream:
    for line in istream:
        line = line.rstrip('\n')
        # 5,5 -> 8,2
        result = re.match('(\d+),(\d+) -> (\d+),(\d+)', line)
        x1 = int(result.group(1))
        y1 = int(result.group(2))
        x2 = int(result.group(3))
        y2 = int(result.group(4))
        segments.append(Line(x1, y1, x2, y2))

print('Part 1: ', part_1(segments))
print('Part 2: ', part_2(segments))
