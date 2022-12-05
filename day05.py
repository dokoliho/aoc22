from functools import reduce
from time import perf_counter as pfc
import re


def read_puzzle(filename):
    with open(filename) as f:
        return [x for x in f]


def split_lines(lines):
    """
    Zerlegen der eingelesenen Zeilen in den Bereich, der
    die Container beschreibt, und in den Berech, der die
    Kranbewegungen beschreibt
    """
    empty_line_pos = lines.index("\n")
    return (lines[:empty_line_pos], lines[empty_line_pos+1:])


def stack_lines_to_lists(stack_lines):
    """
    ['    [D]    \n',
     '[N] [C]    \n',
     '[Z] [M] [P]\n',
     ' 1   2   3 \n']    ->
    [[None, 'D', None], ['N', 'C', None], ['Z', 'M', 'P']]
    """
    return list(map(lambda line: list(map(convert_to_character, batched(line, 4))), stack_lines[:-1]))


def convert_to_character(s):
    """
    " [X] " -> "X"
    """
    m = re.match(r"\[(.)\]", s)
    return m.group(1) if m else None


def stack_lines_to_stacks(stack_lines):
    """
    ['    [D]    \n',
     '[N] [C]    \n',
     '[Z] [M] [P]\n',
     ' 1   2   3 \n']    -->
    {1: ['Z', 'N'], 2: ['M', 'C', 'D'], 3: ['P']}
    """
    stacks = {}
    for s in batched(stack_lines[-1], 4):
        stacks[int(s.strip())] = []
    stack_lists = stack_lines_to_lists(stack_lines)
    stack_lists.reverse()
    for l in stack_lists:
        for index, container in enumerate(l):
            if container is not None:
                stacks[index+1].append(container)
    return stacks


def movement_lines_to_tuple(m_lines):
    """
    [   'move 1 from 2 to 1\n',
        'move 3 from 1 to 3\n',
        'move 2 from 2 to 1\n',
        'move 1 from 1 to 2\n'  ]   ->  [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]
    """
    return list(map(lambda line: convert_to_tuple(line), m_lines))


def convert_to_tuple(s):
    """
    "move 1 from 2 to 1\n" -> (1, 2, 1)
    """
    m = re.match(r"move (\d+) from (\d+) to (\d+)", s)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def batched(s, n):
    """
    Zerlegen eines Strings in Abschnitte fester Länge. Der letzte Abschnitt kann kürzer sein.
    """
    if n < 1:
        raise ValueError('n must be at least one')
    i = 0
    while (i+n <= len(s)):
        next_batch = s[i:i+n]
        i += n
        yield next_batch


def move_crate_between_stacks(source_stack, destination_stack):
    """
    Bewegen eines Containers von einem Stapel zu einem anderen Stapel
    """
    if len(source_stack) == 0:
        raise Exception("Can't move from empty Stack")
    crate = source_stack.pop()
    destination_stack.append(crate)


def do_movement(stacks, movement_tuple):
    """
    Ausführen einer Movement-Anweisung
    Jeder Container wird einzeln bewegt
    """
    source_stack = stacks[movement_tuple[1]]
    destination_stack = stacks[movement_tuple[2]]
    for count in range(0, movement_tuple[0]):
        move_crate_between_stacks(source_stack, destination_stack)


def do_multiple_movement(stacks, movement_tuple):
    """
    Ausführen einer Movement-Anweisung
    Alle Container werden gemeinsam bewegt
    Simuliert durch Einzelbewegung auf einen Zwischenstapel
    """
    storage = []
    source_stack = stacks[movement_tuple[1]]
    destination_stack = stacks[movement_tuple[2]]
    for count in range(0, movement_tuple[0]):
        move_crate_between_stacks(source_stack, storage)
    for count in range(0, movement_tuple[0]):
        move_crate_between_stacks(storage, destination_stack)


def top_line(stacks):
    """
    Ermitteln der obersten Container
    """
    sorted_keys = list(stacks.keys())
    sorted_keys.sort()
    return reduce(lambda s, e: s+stacks[e][-1], sorted_keys, "")


def solve01(lines):
    """
    Ausführung mit Einzelbewegung
    """
    return solve_intern(lines, do_movement)


def solve02(lines):
    """
    Ausführung mit Sammelbewegung
    """
    return solve_intern(lines, do_multiple_movement)


def solve_intern(lines, movement_function):
    """
    Ausführung der Bewegungen
    """
    stack_lines, movements_lines = split_lines(lines)
    stacks = stack_lines_to_stacks(stack_lines)
    movement_tuples = movement_lines_to_tuple(movements_lines)
    for tuple in movement_tuples:
        movement_function(stacks, tuple)
    return top_line(stacks)


if __name__ == '__main__':
    lines = read_puzzle("data/day5.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

