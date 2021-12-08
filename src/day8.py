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
        # sum of the output
        self.result = 0
    def parse_line(self, codes: str, output: str) -> None:
        patterns = {}
        # parse input codes
        for s in codes.split():
            size = len(s)
            if size not in patterns:
                patterns[size] = [set(s)]
            else:
                patterns[size] += [set(s)]

        # confirm that all digits are in the input
        assert(len(patterns) == len(digit_by_len))

        digits = {
            1: patterns[2][0].copy(),
            7: patterns[3][0].copy(),
            8: patterns[7][0].copy(),
            4: patterns[4][0].copy()
        }

        # look for digit 9
        for code in patterns[6]:
            res = (digits[4] | digits[7]) ^ code
            if len(res) == 1:
                digits[9] = code.copy()
                break
        # look for mid
        patterns[6].remove(digits[9]) 
        assert(len(patterns[6]) == 2)

        # find digits 0 and 6:
        if len(patterns[6][0] & digits[1]) == 2:
            digits[0] = patterns[6][0].copy()
            digits[6] = patterns[6][1].copy()
        else:
            digits[0] = patterns[6][1].copy()
            digits[6] = patterns[6][0].copy()
        # 0 1 _ _ 4 _ 6 7 8 9
        
        # look for top-right
        assert(len(digits[8] ^ digits[6]) == 1)
        top_right = (digits[8] ^ digits[6]).pop()

        digits[5] = digits[9] ^ { top_right }
        assert(len(digits[5]) == 5)
        patterns[5].remove(digits[5]) 
        # 0 1 _ _ 4 5 6 7 8 9
        if len(patterns[5][0] & digits[1]) == 2:
            digits[3] = patterns[5][0].copy()
            digits[2] = patterns[5][1].copy()
        else:
            digits[3] = patterns[5][1].copy()
            digits[2] = patterns[5][0].copy()
        
        n = ''
        for value in output.rstrip('\n').split():
            s = set(value)
            for i in range(10):
                if digits[i] == s:
                    n += str(i)
                    break
        self.result += int(n)

part_1 = Part_1()
part_2 = Part_2()
with open('../input/day8.txt') as istream:
    for line in istream:
        splitted = line.split('|')
        part_1.parse_line(splitted[1])
        part_2.parse_line(splitted[0], splitted[1])

print("Part_1: ", part_1.result)
print("Part_2: ", part_2.result)
