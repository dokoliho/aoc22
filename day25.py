from typing import List
import types
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> str:
    """
    Aufaddieren aller Snafus
    """
    snafus = convert(lines)
    result = "0"
    for snafu in snafus:
        result = add_snafus(result, snafu)
    return result


def solve02(lines: List[str]) -> int:
    """
    Not needed
    """
    return 0


def convert(lines):
    """
    Entfernen der Zeilenumbrüche
    """
    return list(map(lambda l: l.strip(), lines))


def snafu_to_dec(snafu):
    """
    Umwandlung eines SNAFU in eine Dezimalzahl
    """
    translation = {"2": 2, "1":1, "0":0, "-":-1, "=":-2}
    sum = 0
    for i in range(len(snafu)-1, -1, -1):
        sum += 5 ** (len(snafu)-1 - i) * translation[snafu[i]]
    return sum


def add_snafus(s1, s2):
    """
    Addieren von zwei Snafus
    """
    mlen = max(len(s1), len(s2))
    s1 = rjust_snafu(s1, mlen+1)
    s2 = rjust_snafu(s2, mlen+1)
    result = list(rjust_snafu("", mlen+1))
    carry = 0
    for i in range(mlen, 0, -1):
        result[i], carry = add_snafu_pos(s1[i], s2[i], carry)
    if carry == -1:
        result[0] = "-"
    if carry == 1:
        result[0] = "1"
    return "".join(result).lstrip("0")


def rjust_snafu(snafu, mlen):
    """
    Auffüllen eines Strings mit 0 von links bis zur vorgegebenen Länge
    """
    format_str = "{" + f"0:0>{mlen}" + "}"
    return format_str.format(snafu)


def add_snafu_pos(p1, p2, carry):
    """
    Addieren von zwei Snafu-Positionen
    """
    alphabet = ["=", "-", "0", "1", "2"]
    w1 = alphabet.index(p1)-2
    w2 = alphabet.index(p2)-2
    sum = w1+w2+carry
    carry = 0
    if sum < -2:
        carry = -1
    if sum > 2:
        carry = 1
    return alphabet[(sum+2) % len(alphabet)], carry


if __name__ == '__main__':
    lines = read_puzzle("data/day25.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
