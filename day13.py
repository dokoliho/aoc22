import copy
import functools
from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    """
    pairs = convert_to_packet_pairs(lines)
    order = list(map(lambda p: check_order(p[0], p[1]), pairs))
    sum = 0
    for index, result in enumerate(order):
        if result:
            sum += (index+1)
    return sum

def solve02(lines: List[str]) -> int:
    """
    """
    divider1 = [[2]]
    divider2 = [[6]]
    packets = convert_lines_to_packets(lines)
    packets.append(divider1)
    packets.append(divider2)
    packets = sorted(packets, key=functools.cmp_to_key(compare))
    index1 = packets.index(divider1)+1
    index2 = packets.index(divider2)+1
    return index1*index2


def convert_to_packet_pairs(lines):
    return list(map(lambda pair: (convert_line_to_packet(pair[0]), convert_line_to_packet(pair[1])), convert_to_pairs(lines)))


def convert_to_pairs(lines):
    pairs = []
    for i in range(0, len(lines), 3):
        pairs.append((lines[i], lines[i+1]))
    return pairs


def convert_lines_to_packets(lines):
    packets = []
    for line in lines:
        if len(line.strip()) > 0:
            packets.append(convert_line_to_packet(line))
    return packets


def convert_line_to_packet(line):
    loc = {}
    exec(f"packet = {line}", globals(), loc)
    return loc['packet']


def compare(packet1, packet2):
    p1 = copy.deepcopy(packet1)
    p2 = copy.deepcopy(packet2)
    check = check_order(p1, p2)
    if check:
        return -1
    if not check:
        return 1
    return 0

def check_order(packet1, packet2):
    if  len(packet1) == 0 and len(packet2) == 0:
        return None
    if len(packet1) == 0:
        return True
    if len(packet2) == 0:
        return False
    element1 = packet1.pop(0)
    element2 = packet2.pop(0)
    if isinstance(element1, int) and isinstance(element2, int):
        if element1 == element2:
            return check_order(packet1, packet2)
        return element1 < element2
    if isinstance(element1, int):
        element1 = [ element1 ]
    if isinstance(element2, int):
        element2 = [ element2 ]
    result = check_order(element1, element2)
    if result is not None:
        return result
    return check_order(packet1, packet2)


if __name__ == '__main__':
    lines = read_puzzle("data/day13.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

