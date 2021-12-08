from functools import reduce

digit_by_len = {
    2: [1],
    3: [7],
    4: [4],
    5: [3,2,5],
    6: [0,6,9],
    7: [8]
}

class Part_1:
    def __init__(self) -> None:
        # how many times digits 1,7,4,8 appear
        self.result = 0
    def parse_line(self, line: str) -> None:
        self.result = reduce(
            lambda a, b: a + int(len(digit_by_len[b]) == 1)
            , [len(s) for s in line.rstrip('\n').split()]
            , self.result
        )

class Part_2:
    def __init__(self) -> None:
        # how many times digits 1,7,4,8 appear
        self.result = 0
    def parse_line(self, left: str, right: str) -> None:
        pass

part_1 = Part_1()
part_2 = Part_2()
with open('../input/day8.txt') as istream:
    for line in istream:
        splitted = line.split('|')
        part_1.parse_line(splitted[1])
        part_2.parse_line(splitted[0], splitted[1])

print("Part_1: ", part_1.result)
print("Part_2: ", part_2.result)
