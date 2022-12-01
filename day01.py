from functools import reduce
from time import perf_counter as pfc

def read_puzzle(filename):
    with open(filename) as f:
        return [x for x in f]


# Idee für den funktionalen Ansatz:
# Die ursprüngliche Liste wird reduziert auf eine Liste mit den Summen
# Dazu wird ein Tupel (current, list) als value durchgereicht, das den aktuellen Summenstand und die bisherige
# Summenliste enthält. Je nach Inhalt des aktuellen Elements wird entweder der Summenstand erhöht
# oder das Ergebnis zur Summenliste hinzugefügt.

def solve(puzzle):
    _, board = reduce(lambda value, element:
                      (value[0]+int(element), value[1]) if element != '\n' else (0, value[1] + [value[0]]),
                      puzzle,
                      (0, []))
    board.sort()
    return sum(board[-3:])


puzzle = read_puzzle("data/Tag_01.txt")
start = pfc()
print(solve(puzzle), pfc()-start)