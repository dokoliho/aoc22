from functools import reduce
from time import perf_counter as pfc


def read_puzzle(filename):
    """
    Einlesen der Inputdaten. Je Zeile zwei Buchstaben. Erster Buchstabe A, B oder C,
    zweiter Buchstabe X, Y, Z. Um später besser damit rechnen zu können, wird jede Zeile in
    ein Tupel aus zwei Integer umgewandelt
    A, X -> 0
    B, Y -> 1
    C, Z -> 2
    Die Tupel werden als Liste zurückgegeben.
    """
    with open(filename) as f:
        pairs = [tuple(x.split()) for x in f]
        return list(map(lambda pair: (ord(pair[0])-ord('A'), ord(pair[1])-ord('X')), pairs))


def value_of_pair(pair_of_moves):
    """
    Das übergebene Tupel enthält die Auswahl des Gegners und des Spielers
    0 -> Stein (gibt bei Auswahl 1 Punkt "Value of Shape")
    1 -> Papier (gibt bei Auswahl 2 Punkte "Value of Shape")
    2 -> Schere (gibt bei Auswahl 3 Punkte "Value of Shape")
    Der Punktwert eines Tupels ergibt sich aus dem "Value of Shape" der eigenen Wahl zzgl.
    der Gewinnprämie (0 bei Loss, 3 bei Draw, 6 bei Win)
    """
    opponent, player = pair_of_moves
    value_of_shape = player + 1
    value_of_match = 3 * (2 - (opponent - player + 1) % 3)
    return value_of_shape + value_of_match


def calculated_player_move(pair_with_strategy):
    """
    Im zweiten Teil des Rätsels enthält das Tupel an der zweiten Stelle nicht mehr die
    Wahl des Spielers, sondern die Vorgabe, ob er verlieren (0), unentschieden spielen (1)
    oder gewinnen (2) soll. Um den entwickelten Algorithmus weiter verwenden zu können,
    muss aus dieser Vorgabe der Spielerzug berechnet werden
    """
    opponent, strat = pair_with_strategy
    return (opponent+strat+2) % 3


def solve(puzzle):
    """
    Bei zweiten Teil des Rätsels müssen die Tupel zunächst überarbeitet werden und
    der Spielerzug eingetragen werden. Danach werden alle Tupelwerte aufsummiert.
    """
    puzzle = list(map(lambda pair: (pair[0], calculated_player_move(pair)), puzzle))
    return reduce(lambda value, element: value + value_of_pair(element), puzzle, 0)


if __name__ == '__main__':
    puzzle = read_puzzle("data/day2.txt")
    start = pfc()
    print(solve(puzzle), pfc()-start)