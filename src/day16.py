from functools import reduce
import time

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

    def consume(self, count: int):
        self.start += count

def handle_literal(generator: Extractor):
    SHIFT = 5

    group = generator.next(SHIFT)
    init = group[1:]
    while group[0] != '0':
        group = generator.next(SHIFT)
        init += group[1:]
    return init

def calc_packet_version(generator: Extractor):
    LITERAL = 4

    packet_version = int(generator.next(3), 2)
    packet_type_id = int(generator.next(3), 2)

    sum = packet_version
    if packet_type_id == LITERAL:
        # just consume string
        handle_literal(generator)
    else:
        length_type_id = int(generator.next(1))
        if length_type_id == 1:
            # number of subpackets
            subpacket_count = int(generator.next(11), 2)
            while subpacket_count > 0:
                sum += calc_packet_version(generator)
                subpacket_count -= 1
        else:
            # number of bits contains in all subpackets
            total_length = int(generator.next(15), 2)
            while total_length > 0:
                start = generator.start
                sum += calc_packet_version(generator)
                total_length -= generator.start - start
    return sum

func_by_id = {
    0: lambda init, literal: init + literal, 
    1: lambda init, literal: init * literal, 
    2: lambda init, literal: init if init < literal else literal, 
    3: lambda init, literal: init if init > literal else literal, 
    5: lambda init, literal: 1 if init > literal else 0, 
    6: lambda init, literal: 1 if init < literal else 0, 
    7: lambda init, literal: 1 if init == literal else 0
}

def calc_packet_value(generator: Extractor):
    LITERAL = 4

    generator.consume(3) # packet_version
    packet_type_id = int(generator.next(3), 2)

    result = None
    if packet_type_id == LITERAL:
        result = int(handle_literal(generator), 2)
    else:
        fn = func_by_id[packet_type_id]
        length_type_id = int(generator.next(1))
        if length_type_id == 1:
            # number of subpackets
            subpacket_count = int(generator.next(11), 2)
            # init result
            result = calc_packet_value(generator)
            while subpacket_count > 1:
                result = fn(result, calc_packet_value(generator))
                subpacket_count -= 1
        else:
            # number of bits contains in all subpackets
            total_length = int(generator.next(15), 2)
            # init result
            start = generator.start
            result = calc_packet_value(generator)
            total_length -= generator.start - start
            while total_length > 0:
                start = generator.start
                result = fn(result, calc_packet_value(generator))
                total_length -= generator.start - start
    return result

def part_1(generator: Extractor):
    return calc_packet_version(generator)

def part_2(generator: Extractor):
    return calc_packet_value(generator)

binary = str()
with open("../input/day16.txt") as istream:
    accumulator = lambda init, token: init + bin(int(token, 16))[2:].zfill(4)
    binary = reduce(accumulator, istream.readline().rstrip('\n'), binary)

begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(Extractor(binary)), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(Extractor(binary)), time.time() - begin))
