from typing import List
from day20 import solve01, solve02, convert, do_all_movements, do_movement, calc_sequence, apply_decryption_key
from day20 import alt_impl, solve01alt, solve02alt

def data() -> List[str]:
    return [
        '1\n',
        '2\n',
        '-3\n',
        '3\n',
        '-2\n',
        '0\n',
        '4\n',
    ]


def test_convert():
    lines = data()
    nums = convert(lines)
    assert len(nums) == 7
    assert nums[-1] == 4


def test_one_encrypted_mix_agaist_alt_impl():
    lines = data()
    nums = convert(lines)
    nums = apply_decryption_key(nums, 811589153)
    correct = alt_impl(nums)
    offsets = [ 0 for _ in range(len(nums))]
    for index, num in enumerate(nums):
        offsets = do_movement(index, num, offsets)
    assert calc_sequence(nums, offsets) == correct


def test_do_all_movements():
    lines = data()
    nums = convert(lines)
    nums = do_all_movements(nums)
    assert nums == [1, 2, -3, 4, 0, 3, -2]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 3


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 1623178306


def test_solve1_alt():
    lines: List[str] = data()
    result: int = solve01alt(lines)
    assert result == 3


def test_solve2_alt():
    lines: List[str] = data()
    result: int = solve02alt(lines)
    assert result == 1623178306
