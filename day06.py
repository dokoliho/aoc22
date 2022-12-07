
from time import perf_counter as pfc



def read_puzzle(filename):
    with open(filename) as f:
        return [x for x in f]




def solve01(lines):
    """
    Ermitteln des ersten Blocks mit 4 unterschiedlichen Zeichen
    """
    signal = lines[0]
    return find_different_chars(signal, 4)


def solve02(lines):
    """
    Ermitteln des ersten Blocks mit 14 unterschiedlichen Zeichen
    """
    signal = lines[0]
    return find_different_chars(signal, 14)


def find_different_chars(s, n):
    """
    Ermitteln des ersten Blocks mit n unterschiedlichen Zeichen in s
    """
    first_tuple = next(filter(lambda tuple: has_diff_elements(tuple[0]), sliding_window_with_end(s, n)))
    return first_tuple[1]


def has_diff_elements(l):
    """
    True, falls die übergeben Liste aus lauter unterschiedlichen Elementen besteht
    """
    return len(l) == len(set(l))


def sliding_window_with_end(s, n):
    """
    Bewegen eines Fensters der Länge n über einen String.
    Rückgabe der Zeichen als Liste
    """
    if n < 1:
        raise ValueError('n must be at least one')
    i = 0
    while (i+n <= len(s)):
        result = (list(s[i:i+n]), i+n)
        i += 1
        yield result


if __name__ == '__main__':
    lines = read_puzzle("data/day6.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

