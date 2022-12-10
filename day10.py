from typing import List, Any
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Summe der Signalstärken im Cycle 20, 60, 100, 140, 180 und 220
    """
    commands = convert(lines)
    values = list(register_values(commands))
    return sum(map(lambda cycle: signal_strength(cycle, values), range(20, 221, 40)))


def solve02(lines: List[str]) -> int:
    """
    Ausgabe der 6 Zeilen des Displays
    """
    commands = convert(lines)
    values = list(register_values(commands))
    print()
    for line_index in range(6):
        print(get_line(line_index, values))
    return 0


def convert(lines: List[str]):
    """
    ['addx 15\n', 'addx -11\n',  'noop\n'] ->
    [('addx', 15), ('addx', -11),  ('noop', None)]
    """
    return list(map(lambda l: convert_line_to_tuple(l.strip()), lines))


def convert_line_to_tuple(line):
    """
    Konvertierung eines einzelenen Tupels
    """
    if line == "noop":
        return "noop", None
    tup = tuple(line.split())
    return tup[0], int(tup[1])


def register_values(commands):
    """
    Generator für die Registerwerte
    Startwert ist 1
    """
    x = 1
    for command in commands:
        if command[0] == "noop":
            yield x
        else:
            yield x
            yield x
            x += command[1]


def signal_strength(cycle, values):
    """
    Signalstärke in einem Cycle
    """
    return values[cycle-1] * cycle


def get_line(i, values):
    """
    Berechning der i. Zeile
    """
    start_cycle = i * 40
    line = ""
    for i in range(start_cycle, start_cycle+40):
        position = values[i]
        diff = abs(i-position-start_cycle)
        line += "#" if diff < 2 else '.'
    return line


if __name__ == '__main__':
    lines = read_puzzle("data/day10.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

