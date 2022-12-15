from typing import List
from day15 import solve01, solve02, convert_to_sensor_map, cover_in_line, covered_intervals_in_line, len_of_intervals, len_of_intervals_without_beacons


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
    result = convert_to_sensor_map(data())
    assert len(result) == 14
    assert result[0] == (2, 18, -2, 15)


def test_cover_in_line():
    sensors = convert_to_sensor_map(data())
    r = cover_in_line(sensors[6], 7)
    assert -2 not in r
    assert -1 in r
    assert 17 in r
    assert 18 not in r
    r = cover_in_line(sensors[6], 2)
    assert 3 not in r
    assert 4 in r
    assert 12 in r
    assert 13 not in r
    r = cover_in_line(sensors[6], 16)
    assert 7 not in r
    assert 8 in r
    assert 9 not in r


def test_covered_intervals_in_line():
    sensors = convert_to_sensor_map(data())
    intervals = covered_intervals_in_line(sensors, 10)
    l = len_of_intervals(intervals)
    assert l == 27
    l = len_of_intervals_without_beacons(sensors, intervals, 10)
    assert l == 26




def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
