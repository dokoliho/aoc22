from typing import List, Tuple
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    """
    nums = convert(lines)
    nums = do_all_movements(nums)
    pos = nums.index(0)
    return sum([nums[(pos + index) % len(nums)] for index in range(1000, 3001, 1000)])


def solve02(lines: List[str]) -> int:
    """
    """
    nums = convert(lines)
    dec_nums = apply_decryption_key(nums, 811589153)
    mixed_nums = do_all_movements(dec_nums, 10)
    pos = mixed_nums.index(0)
    return sum([mixed_nums[(pos + index) % len(mixed_nums)] for index in range(1000, 3001, 1000)])


def solve01alt(lines: List[str]) -> int:
    """
    """
    nums = convert(lines)
    nums = alt_impl(nums)
    pos = nums.index(0)
    return sum([nums[(pos + index) % len(nums)] for index in range(1000, 3001, 1000)])


def solve02alt(lines: List[str]) -> int:
    """
    """
    nums = convert(lines)
    dec_nums = apply_decryption_key(nums, 811589153)
    mixed_nums = alt_impl(dec_nums, 10)
    pos = mixed_nums.index(0)
    return sum([mixed_nums[(pos + index) % len(mixed_nums)] for index in range(1000, 3001, 1000)])


def convert(lines):
    """
    """
    return list(map(lambda l: int(l.strip()), lines))


def apply_decryption_key(nums, key):
    return list(map(lambda n: n * key, nums))


def do_all_movements(nums, count=1):
    offsets = [ 0 for _ in range(len(nums))]
    for _ in range(count):
        for index, num in enumerate(nums):
            do_movement(index, num, offsets)
    return calc_sequence(nums, offsets)


def alt_impl(data, count=1):
    orig = list(enumerate(data))
    nums = orig.copy()
    for _ in range(count):
        for n in orig:
            old_idx = nums.index(n)
            new_idx = (old_idx + n[1]) % (len(nums) - 1)
            del nums[old_idx]
            nums.insert(new_idx, n)
    return list(map(lambda tup: tup[1], nums))

def calc_sequence(nums, offsets):
    transitions = list(map(lambda tup: (tup[0], (sum(tup)) % len(offsets)), enumerate(offsets)))
    transitions.sort(key=lambda tup: tup[1])
    return list(map(lambda t: nums[t[0]], transitions))


def check_consistency(nums, offsets):
    transitions = list(map(lambda tup: (tup[0], (sum(tup)) % len(offsets)), enumerate(offsets)))
    indx = list(map(lambda tup: tup[1], transitions))
    indx.sort()
    for i in range(len(indx)):
        assert i == indx[i]


def do_movement(index, num, offsets):
    if num == 0:
        return offsets
    mod = len(offsets)
    curr_pos = mod_value(index + offsets[index], mod)
    next_pos = calc_new_pos(curr_pos, num, mod)
    for i, offset in enumerate(offsets):
        if curr_pos < next_pos:
            if curr_pos < mod_value(i+offset, mod) <= next_pos:
                offsets[i] -= 1
        if curr_pos > next_pos:
            if next_pos <= mod_value(i+offset, mod) < curr_pos:
                offsets[i] += 1
    offsets[index] += (next_pos - curr_pos)
    return offsets


def calc_new_pos(current, offset, mod):
    if offset == 0:
        return current
    if offset > 0:
        return shift_pos(current, offset, mod)
    else:
        return shift_neg(current, offset, mod)


def shift_pos(current, offset, mod):
    overflow_count = (current + offset) // mod
    return (current + offset + overflow_count) % mod


def shift_neg(current, offset, mod):
    x = abs(current + offset - mod)
    underflow_count = x // mod
    return (current + offset + underflow_count * mod - underflow_count ) % mod


def mod_value(value, mod):
    return (value + mod) % mod


if __name__ == '__main__':
    lines = read_puzzle("data/day20.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
