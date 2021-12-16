from functools import reduce
import time
from typing import Generator

class Extractor:
    binary: str
    start: int

    def __init__(self, binary: str) -> None:
        self.binary = binary
        self.start = 0

    def next(self, count: int):
        ret = self.binary[self.start: self.start + count]
        self.start += count
        return ret

def handle_literal(generator: Extractor):
    shift = 5
    stop = lambda bits: bits[0] == '0'
    update = lambda init, next: init + next[1:]

    bit_used = 6 # packet's version (3) and packet's ID (3)
    group = generator.next(shift)
    init = group[1:]
    bit_used += 5
    while not stop(group):
        group = generator.next(shift)
        init = update(init, group)
        bit_used += 5
    # consume padding 
    # padding = (4 - (bit_used % 4)) % 4
    # generator.next(padding)
    return init

def handle_packet(generator: Extractor, depth: int):
    LITERAL = 4
    # PREFIX = '  ' * depth

    packet_version = int(generator.next(3), 2)
    packet_type_id = int(generator.next(3), 2)

    # print(PREFIX, '{')
    # print(PREFIX, "  Version", packet_version)
    # print(PREFIX, "  Type id", packet_type_id)

    sum = packet_version
    if packet_type_id == LITERAL:
        # print(PREFIX, "  Literal")
        # skip literal
        handle_literal(generator)
    else:
        length_type_id = int(generator.next(1))
        if length_type_id == 1:
            # number of subpackets
            subpacket_count = int(generator.next(11), 2)
            # print(PREFIX, "  Operator {} subpackets".format(subpacket_count))
            while subpacket_count > 0:
                # assume it's only literals!!!
                sum += handle_packet(generator, depth + 1)
                subpacket_count -= 1
        else:
            # number of bits contains in all subpackets
            subbin = generator.next(15)
            total_length = int(subbin, 2)
            # print(PREFIX, "  Operator {} total length".format(total_length))
            while total_length > 0:
                start = generator.start
                sum += handle_packet(generator, depth + 1)
                total_length -= generator.start - start
    # print(PREFIX, '}')
    return sum

def part_1(generator: Extractor):
    return handle_packet(generator, 0)

def part_2(generator: Extractor):
    pass

binary = str()
with open("../input/day16.txt") as istream:
    accumulator = lambda init, token: init + bin(int(token, 16))[2:].zfill(4)
    binary = reduce(accumulator, istream.readline().rstrip('\n'), binary)
    # print(binary)

# {011 000 1 00000000010 {<1st> 000 000 0 000000000010110 { 000 100 01010 } { 101 100 01011 } } {<2nd> 001 000 1 00000000010 { 000 100 01100 } { 011 100 01101 00}}}


begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(Extractor(binary)), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(Extractor(binary)), time.time() - begin))
