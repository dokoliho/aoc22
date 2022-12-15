from typing import List
from day15 import solve01, solve02, convert_to_sensors, disjunct_cover_intervals_in_line
from day15 import len_of_intervals, is_line_possible, free_intervals
from day15 import covered_interval_in_line_by_one_sensor


def data() -> List[str]:
    return [
        'Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n',
        'Sensor at x=9, y=16: closest beacon is at x=10, y=16\n',
        'Sensor at x=13, y=2: closest beacon is at x=15, y=3\n',
        'Sensor at x=12, y=14: closest beacon is at x=10, y=16\n',
        'Sensor at x=10, y=20: closest beacon is at x=10, y=16\n',
        'Sensor at x=14, y=17: closest beacon is at x=10, y=16\n',
        'Sensor at x=8, y=7: closest beacon is at x=2, y=10\n',
        'Sensor at x=2, y=0: closest beacon is at x=2, y=10\n',
        'Sensor at x=0, y=11: closest beacon is at x=2, y=10\n',
        'Sensor at x=20, y=14: closest beacon is at x=25, y=17\n',
        'Sensor at x=17, y=20: closest beacon is at x=21, y=22\n',
        'Sensor at x=16, y=7: closest beacon is at x=15, y=3\n',
        'Sensor at x=14, y=3: closest beacon is at x=15, y=3\n',
        'Sensor at x=20, y=1: closest beacon is at x=15, y=3\n',
    ]


def test_convert():
    result = convert_to_sensors(data())
    assert len(result) == 14
    assert result[0] == (2, 18, -2, 15)


def test_cover_in_line():
    sensors = convert_to_sensors(data())
    lower, upper = covered_interval_in_line_by_one_sensor(sensors[6], 7)
    r = range(lower, upper+1)
    assert -2 not in r
    assert -1 in r
    assert 17 in r
    assert 18 not in r
    lower, upper = covered_interval_in_line_by_one_sensor(sensors[6], 2)
    r = range(lower, upper+1)
    assert 3 not in r
    assert 4 in r
    assert 12 in r
    assert 13 not in r
    lower, upper = covered_interval_in_line_by_one_sensor(sensors[6], 16)
    r = range(lower, upper+1)
    assert 7 not in r
    assert 8 in r
    assert 9 not in r


def test_covered_intervals_in_line():
    sensors = convert_to_sensors(data())
    intervals = disjunct_cover_intervals_in_line(sensors, 10)
    l = len_of_intervals(intervals)
    assert l == 27



def test_is_line_possible():
    sensors = convert_to_sensors(data())
    assert is_line_possible(sensors, 11, 20)
    assert not is_line_possible(sensors, 10, 20)


def test_free_intervals():
    sensors = convert_to_sensors(data())
    intervals = disjunct_cover_intervals_in_line(sensors, 11)
    intervals = sorted(intervals, key=lambda tup: tup[0])
    free = free_intervals(intervals, 0, 20)
    assert len(free) == 1
    assert free[0] == (14, 14)


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines, 10)
    assert result == 26


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines, 20)
    assert result == 56000011
