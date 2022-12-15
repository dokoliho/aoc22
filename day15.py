import math
from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    """
    sensors = convert_to_sensor_map(lines)
    list_of_intervals = covered_intervals_in_line(sensors, 2000000)
    return len_of_intervals_without_beacons(sensors, list_of_intervals, 2000000)


def len_of_intervals(list_of_intervals):
    return sum(map(len_interval, list_of_intervals))


def len_of_intervals_without_beacons(sensors, list_of_intervals, line):
    return sum(map(lambda i: len_interval_without_beacons(sensors, i, line), list_of_intervals))


def len_interval(interval):
    return interval[1]-interval[0]+1


def len_interval_without_beacons(sensors, interval, line):
    raw = len_interval(interval)
    beacons_in_interval = set()
    for sensor in sensors:
        if sensor[3] == line:
            if interval[0] <= sensor[2] <= interval[1]:
                beacons_in_interval.add(sensor[2])
    return raw - len(beacons_in_interval)



def solve02(lines: List[str]) -> int:
    """
    """
    return 0


def convert_to_sensor_map(lines: List[str]):
    return list(map(lambda line: convert_line_to_tuple(line.strip()), lines))


def convert_line_to_tuple(line):
    m = re.search(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$", line)
    return tuple(map(int, m.groups()))


def map_size(sensors):
    x_min = math.inf
    x_max = -math.inf
    y_min = math.inf
    y_max = -math.inf
    for sensor in sensors:
        x_min = min(x_min, sensor[0] - manhattan_distance(sensor))
        y_min = min(y_min, sensor[1] - manhattan_distance(sensor))
        x_max = max(x_max, sensor[0] + manhattan_distance(sensor))
        y_max = max(y_max, sensor[1] + manhattan_distance(sensor))
    return x_min, y_min, x_max, y_max


def manhattan_distance(sensor):
    return abs(sensor[0]-sensor[2]) + abs(sensor[1]-sensor[3])


def covering_sensors(sensors, line):
    return [sensor for sensor in sensors if is_covering(sensor, line)]


def is_covering(sensor, line):
    return sensor[1] - manhattan_distance(sensor) <= line <= sensor[1] + manhattan_distance(sensor)


def cover_in_line(sensor, line):
    lower, upper = covered_interval_in_line(sensor, line)
    return range(lower, upper+1)


def covered_interval_in_line(sensor, line):
    y_diff = abs(sensor[1] - line)
    remaining = manhattan_distance(sensor) - y_diff
    return sensor[0] - remaining, sensor[0] + remaining


def covered_intervals_in_line(sensors, line):
    sensors = covering_sensors(sensors, line)
    intervals = []
    for sensor in sensors:
        intervals.append(covered_interval_in_line(sensor, line))
    while(True):
        l = len(intervals)
        intervals = simplify_intervals(intervals, [])
        if len(intervals) == l: break
    return intervals


def simplify_intervals(intervals, simplified):
    if len(intervals) == 0:
        return simplified
    new_interval = intervals.pop(0)
    for interval in simplified:
        if interval[0] <= new_interval[0] and interval[1] >= new_interval[1]:
            return simplify_intervals(intervals, simplified)
        if interval[0] >= new_interval[0] and interval[1] <= new_interval[1]:
            new_simplified = [i for i in simplified if not i == interval]
            new_simplified.append((new_interval[0], new_interval[1]))
            return simplify_intervals(intervals, new_simplified)
        if interval[0] <= new_interval[0]:
            new_simplified = [i for i in simplified if not i == interval]
            new_simplified.append((interval[0], new_interval[1]))
            return simplify_intervals(intervals, new_simplified)
        if interval[1] >= new_interval[1]:
            new_simplified = [i for i in simplified if not i == interval]
            new_simplified.append((new_interval[0], interval[1]))
            return simplify_intervals(intervals, new_simplified)
    simplified.append(new_interval)
    return simplify_intervals(intervals, simplified)


if __name__ == '__main__':
    lines = read_puzzle("data/day15.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

