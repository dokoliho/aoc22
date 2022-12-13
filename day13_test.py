import functools
from typing import List
from day13 import solve01, solve02, convert_to_packet_pairs, check_order, convert_lines_to_packets, compare


def data() -> List[str]:
    return [
        '[1,1,3,1,1]\n',
        '[1,1,5,1,1]\n',
        '\n',
        '[[1],[2,3,4]]\n',
        '[[1],4]\n',
        '\n',
        '[9]\n',
        '[[8,7,6]]\n',
        '\n',
        '[[4,4],4,4]\n',
        '[[4,4],4,4,4]\n',
        '\n',
        '[7,7,7,7]\n',
        '[7,7,7]\n',
        '\n',
        '[]\n',
        '[3]\n',
        '\n',
        '[[[]]]\n',
        '[[]]\n',
        '\n',
        '[1,[2,[3,[4,[5,6,7]]]],8,9]\n',
        '[1,[2,[3,[4,[5,6,0]]]],8,9]\n',
     ]


def test_convert_to_packet_pairs():
    lines = data()
    result = convert_to_packet_pairs(lines)
    assert len(result) == 8


def test_check_order():
    lines = data()
    pairs = convert_to_packet_pairs(lines)
    result = list(map(lambda p: check_order(p[0], p[1]), pairs))
    assert result == [True, True, False, True, False, True, False, False]


def test_sorted_packages():
    lines = data()
    packets = convert_lines_to_packets(lines)
    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=functools.cmp_to_key(compare))
    assert packets == [
        [],
        [[]],
        [[[]]],
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [[1], 4],
        [[2]],
        [3],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [[6]],
        [7, 7, 7],
        [7, 7, 7, 7],
        [[8, 7, 6]],
        [9],
    ]

def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 13


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 140
