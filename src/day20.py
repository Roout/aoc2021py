import time
from typing import List

SHIFTS = [
    (-1,-1), (0,-1), (1,-1),
    (-1, 0), (0, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)]

def get_pixel(input: List[str], x: int, y: int, flipped: bool):
    height = len(input)
    width = len(input[0])

    if x < 0 or x >= width:
        return '#' if flipped else '.'
    if y < 0 or y >= height:
        return '#' if flipped else '.'
    return input[y][x] 

def encode_image(input: List, algo: str, flipped: bool):
    height = len(input) + 2
    width = len(input[0]) + 2
    image = list()
    for y in range(height):
        image += [['.'] * width]
        for x in range(width):
            sequence = ''
            for shift in SHIFTS:
                next_x = x + shift[0]
                next_y = y + shift[1]
                pixel = get_pixel(input, next_x - 1, next_y - 1, flipped)
                sequence += '0' if pixel == '.' else '1'
            index = int(sequence, 2)
            image[y][x] = algo[index]
    image[:] = (''.join(row) for row in image)
    return image

def dump_image(image: List[str]):
    for row in image:
        print(row)
    print('')

def count_lit(image):
    lit = 0
    for row in image:
        for ch in row:
            lit += ch == '#'
    return lit

def part_1(input: List, algo: str):
    image = input
    for i in range(2):
        image = encode_image(image, algo, i % 2 == 1)
    return count_lit(image)

def part_2(input: List, algo: str):
    image = input
    for i in range(50):
        image = encode_image(image, algo, i % 2 == 1)
    return count_lit(image)

algo = ''
input = list([str])
with open("../input/day20.txt") as istream:
    for line in istream:
        line = line.rstrip()
        if len(line) == 0:
            input = [x.rstrip() for x in istream.readlines()]
        else:
            algo += line

    
begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(input, algo), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(input, algo), time.time() - begin))
