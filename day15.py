import math
from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str], row: int) -> int:
    """
    Ermitteln der Anzahl der garantiert Beacon-freien Plätze in einer Zeile
    """
    sensors = convert_to_sensors(lines)
    intervals = disjunct_cover_intervals_in_line(sensors, row)
    return len_of_intervals(intervals) - count_beacons_in_row(sensors, row)


X_SENSOR = 0
Y_SENSOR = 1
X_NEXT_BEACON = 2
Y_NEXT_BEACON = 3

def convert_to_sensors(lines: List[str]):
    """
    Umwandeln des Inputs in eine Liste von 4-er Tupeln mit dem Aufbau
    (x_sensor, y_sensor, x_next_beacon, y_next_beacon)
    """
    return list(map(lambda line: convert_line_to_tuple(line.strip()), lines))


def convert_line_to_tuple(line):
    """
    Konvertieren einer einzelnen Input-Zeile in ein Tupel
    """
    m = re.search(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$", line)
    return tuple(map(int, m.groups()))


def disjunct_cover_intervals_in_line(sensors, line):
    """
    Rückgabe einer disjunkten Liste von Intervallen, in denen auf Basis der übergebenen Sensoren keine
    unentdeckten Beacons sein können (entdeckte schon)
    """
    sensors = covering_sensors(sensors, line)
    intervals = []
    for sensor in sensors:
        intervals.append(covered_interval_in_line_by_one_sensor(sensor, line))
    return reduced(intervals)


def reduced(intervals):
    """
    Wiederholtes Durchlaufen der Liste der Intervalle mit Zusammenführen überlappender Intervalle
    Die Rekursion bricht ab, wenn bei einem Durchlauf keine Zusammenführungen (mehr) passiert sind
    """
    len_before_merge = len(intervals)
    intervals = merge_intervals(intervals, [])
    if len_before_merge == len(intervals):
        return intervals
    return reduced(intervals)


def merge_intervals(intervals, merged_intervals):
    """
    Rekursives Zusammenführen überlappender Intervalle
    Die Intervalle aus intervals werden sukzessive nach merged_intervals übernommen und dabei
    ggf. mit einem dort bereits vorhandenen Intervall verschmolzen
    """
    if len(intervals) == 0:
        # Abbruch der Rekursion
        return merged_intervals
    new_interval = intervals.pop(0)
    for interval in merged_intervals:
        if interval[0] <= new_interval[0] and interval[1] >= new_interval[1]:
            # neues Intervall komplett in einem bestehenden Interval enthalten
            return merge_intervals(intervals, merged_intervals)
        if interval[0] >= new_interval[0] and interval[1] <= new_interval[1]:
            # bestehendes Intervall komplett im neuen Interval enthalten
            new_merged = [i for i in merged_intervals if not i == interval]
            new_merged.append((new_interval[0], new_interval[1]))
            return merge_intervals(intervals, new_merged)
        if interval[0] <= new_interval[0] <= interval[1]:
            # neues Intervall beginnt in einem bestehenden
            new_merged = [i for i in merged_intervals if not i == interval]
            new_merged.append((interval[0], new_interval[1]))
            return merge_intervals(intervals, new_merged)
        if interval[0] <= new_interval[1] <= interval[1]:
            # neues Intervall endet in einem bestehenden
            new_merged = [i for i in merged_intervals if not i == interval]
            new_merged.append((new_interval[0], interval[1]))
            return merge_intervals(intervals, new_merged)
    # Mit keinem Intervall wurden Überschneidungen gefunden -> neues Intervall zur Liste hinzufügen
    merged_intervals.append(new_interval)
    return merge_intervals(intervals, merged_intervals)


def covering_sensors(sensors, line):
    """
    Ermitteln aller Sensoren, die in der gegebenen Zeile Positionen für Beacons ausschließen
    """
    return [sensor for sensor in sensors if is_covering(sensor, line)]


def is_covering(sensor, line):
    """
    True, falls der übergebene Sensor in der übergebenen Zeile Positionen für Beacons ausschließt
    Ist gegeben, wenn der Abstand zwischen der Sensor-Zeile und der übergebenen Zeile kleiner als
    der Abstand zum entdeckten Beacon ist
    """
    return sensor[Y_SENSOR] - manhattan_distance(sensor) <= line <= sensor[Y_SENSOR] + manhattan_distance(sensor)


def covered_interval_in_line_by_one_sensor(sensor, line):
    """
    Berechnung des Intervalls in einer gegebenen Zeile,
    in dem für einen gegebenen Sensor kein Beacon sein kann
    (bzw. nur das dem Sensor nächstgelegene)
    """
    y_diff = abs(sensor[Y_SENSOR] - line)
    remaining = manhattan_distance(sensor) - y_diff
    return sensor[X_SENSOR] - remaining, sensor[X_SENSOR] + remaining


def count_beacons_in_row(sensors, row):
    """
    Ermitteln der ANzahl endeckter Beacons in einer Zeile
    Ein Beacon kann von mehreren Sensoren entdeckt sein, daher muss eine Verdichtung vorgenommen werden
    """
    return len(set(map(lambda s: s[X_NEXT_BEACON], filter(lambda s: s[Y_NEXT_BEACON] == row, sensors))))


def len_of_intervals(list_of_intervals):
    """
    Aufaddieren der Längen disjunkter Intervalle
    """
    return sum(map(len_interval, list_of_intervals))


def len_interval(interval):
    """
    Ermitteln der Länge eines Intervalls
    """
    return interval[1]-interval[0]+1


def solve02(lines: List[str], upper_bound) -> int:
    """
    Ermitteln der Position eines unentdeckten Beacons
    in den Zeilen 0 bis upper_bound
    Berechnen der Frequenz
    """
    sensors = convert_to_sensors(lines)
    x, y = get_free_position(sensors, upper_bound)
    return x * 4000000 + y


def get_free_position(sensors, max_dim):
    """
    Ermitteln der einen freien Position in den Zeilen 0 bis max_dim
    """
    for y in range(0, max_dim+1):
        intervals = joined_intervals(sensors, y)
        free = free_intervals(intervals, 0, max_dim)
        if len(free) == 0:
            # keine freie Position -> nächste Zeile
            continue
        if len(free) == 1:
            if free[0][0] != free[0][1]:
                raise Exception("Free interval has len > 1")
            return free[0][0], y
        raise Exception("More than 1 free interval")
    return None, None


def joined_intervals(sensors, line):
    list_of_intervals = disjunct_cover_intervals_in_line(sensors, line)
    list_of_intervals = sorted(list_of_intervals, key=lambda tup: tup[0])
    return join_intervals(list_of_intervals, [])


def join_intervals(intervals, joined):
    if len(intervals) == 0:
        return joined
    new_interval = intervals.pop(0)
    if len(joined) == 0:
        return join_intervals(intervals, [new_interval])
    if joined[-1][1]+1 == new_interval[0]:
        new_joined = joined[:-2]
        new_joined.append((joined[-1], new_interval[1]))
        return join_intervals(intervals, joined)
    joined.append(new_interval)
    return join_intervals(intervals, joined)


def is_line_possible(sensors, line, max_dim):
    list_of_intervals = joined_intervals(sensors, line)
    return is_line_possible_with_intervals(list_of_intervals, max_dim)

def is_line_possible_with_intervals(list_of_intervals, max_dim):
    line_possible = True
    for interval in list_of_intervals:
        if interval[0] <= 0 <= interval[1]:
            if interval[1] >= max_dim:
                line_possible = False
                break
    return line_possible





def free_intervals(sorted_intervals, lower_bound, upper_bound):
    if lower_bound > upper_bound:
        return []
    if len(sorted_intervals) == 0:
        return [(lower_bound, upper_bound)]
    interval = sorted_intervals.pop(0)
    if interval[0] <= lower_bound:
        if interval[1] < lower_bound:
            return free_intervals(sorted_intervals, lower_bound, upper_bound)
        else:
            return free_intervals(sorted_intervals, interval[1]+1, upper_bound)
    if upper_bound >= interval[0]:
        return [(lower_bound, interval[0]-1)] + free_intervals(sorted_intervals, interval[1]+1, upper_bound)
    else:
        return [(lower_bound, upper_bound)]


def manhattan_distance(sensor):
    """
    Ermitteln des Manhattan-Abstands zwischen einem Sensor und dem von ihm lokalisierten Beacon
    """
    return abs(sensor[X_SENSOR]-sensor[X_NEXT_BEACON]) + abs(sensor[Y_SENSOR]-sensor[Y_NEXT_BEACON])


if __name__ == '__main__':
    lines = read_puzzle("data/day15.txt")
    start = pfc()
    print(solve01(lines, 2000000), pfc()-start)
    start = pfc()
    print(solve02(lines, 4000000), pfc()-start)

