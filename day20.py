from typing import List, Tuple
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Berechnen eines Durchgangs
    """
    nums = convert(lines)
    nums = do_all_movements(nums)
    pos = nums.index(0)
    return sum([nums[(pos + index) % len(nums)] for index in [1000, 2000, 3000]])


def solve02(lines: List[str]) -> int:
    """
    Anwenden des Keys, Berechnen von 10 Durchgängen
    """
    nums = convert(lines)
    dec_nums = apply_decryption_key(nums, 811589153)
    mixed_nums = do_all_movements(dec_nums, 10)
    pos = mixed_nums.index(0)
    return sum([mixed_nums[(pos + index) % len(mixed_nums)] for index in [1000, 2000, 3000]])


def convert(lines):
    """
    Umwandeln einer Eingabezeile in einen Integer
    """
    return list(map(lambda l: int(l.strip()), lines))


def apply_decryption_key(nums, key):
    """
    Anwendung eines Keys
    """
    return list(map(lambda n: n * key, nums))


def do_all_movements(nums, count=1):
    """
    Durchführung der gegebenen Anzahl der Mixes
    Es werden nicht die Daten getauscht, sondern ein separates Offset-Array berechnet, das
    für jede Stelle anschließend der Verschiebung enthält
    Am Ende wird aus der Ursprungsliste und dem Offset-Array eine Ergebnisliste berechnet
    """
    offsets = [ 0 for _ in range(len(nums))]
    for _ in range(count):
        for index, num in enumerate(nums):
            do_movement(index, num, offsets)
    return calc_sequence(nums, offsets)


def calc_sequence(nums, offsets):
    """
    Berechnen der Ergebnisliste aus der Ursprungsliste und den Offsets
    """
    # Generierung einer Tupelliste (ursprüngliche Position, Endposition)
    transitions = list(map(lambda tup: (tup[0], (sum(tup)) % len(offsets)), enumerate(offsets)))
    # Sortieren nach der Endposition
    transitions.sort(key=lambda tup: tup[1])
    # Wert über die Ursprungsposition einsteuern
    return list(map(lambda t: nums[t[0]], transitions))


def do_movement(index, num, offsets):
    """
    Durchführung einer einzelnen Vertauschung
    in Form von Korrekturen im Offset-Array
    """
    if num == 0:
        return offsets
    mod = len(offsets)
    # Berechnung der aktuellen Elementposition (mod Arraylänge)
    curr_pos = mod_value(index + offsets[index], mod)
    # Berechnen der zukünftigen Elementposition (mod Arraylänge)
    next_pos = calc_new_pos(curr_pos, num, mod)
    # Alle Elemente zwischen diesen Positionen müssen verschoben werden
    for i, offset in enumerate(offsets):
        # nach links, wenn das Element selbst nach rechts geschoben wird
        if curr_pos < next_pos:
            if curr_pos < mod_value(i+offset, mod) <= next_pos:
                offsets[i] -= 1
        # nach rechts, wenn das Element selbst nach links geschoben wird
        if curr_pos > next_pos:
            if next_pos <= mod_value(i+offset, mod) < curr_pos:
                offsets[i] += 1
    # Eintragen der Elementverschiebung selbst
    offsets[index] += (next_pos - curr_pos)
    return offsets


def calc_new_pos(current, offset, mod):
    """
    Berechnung der neuen Elementposition.
    Das hat mich Stunden gekostet
    Man muss verstehen, dass Verschiebungen über den Arrayrand hinaus nicht einfach mod Arraylänge
    gerechnet werden können, weil das Array zu diesem Zeitpunkt um ein Element kürzer ist (das wir
    gerade verschieben)
    """
    if offset == 0:
        return current
    if offset > 0:
        return shift_pos(current, offset, mod)
    else:
        return shift_neg(current, offset, mod)


def shift_pos(current, offset, mod):
    """
    Verschiebung nach rechts.
    Für jeden Umbruch über das verkürzte Array
    müssen wir im Ursprungsarray eine Stelle weiter.
    Daher wird der Overflow-Count addiert
    """
    shorter_array_len = mod - 1
    overflow_count = (current + offset) // shorter_array_len
    return (current + offset + overflow_count) % mod


def shift_neg(current, offset, mod):
    """
    Verschiebung nach links,
    Für jeden Umbruch über das verkürzte Array
    müssen wir im Ursprungsarray eine Stelle weniger weit.
    Daher wird der Underflow-Count abgezogen
    Um sicher positiv zu sein, wird mehrfach die Arraylänge addiert,
    was anschließend durch die Modulo-Rechnung wegfällt.
    """
    shorter_array_len = mod - 1
    x = abs(current + offset - shorter_array_len)
    underflow_count = x // shorter_array_len
    return (current + offset + underflow_count * mod - underflow_count ) % mod


def mod_value(value, mod):
    """
    Positive Modulorechnung
    """
    return (value + mod) % mod


if __name__ == '__main__':
    lines = read_puzzle("data/day20.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
