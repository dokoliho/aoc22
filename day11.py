from functools import reduce
from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    20 Runden Monkey Business
    """
    return solve(lines, Monkey, 20)


def solve02(lines: List[str]) -> int:
    """
    10000 Runden Monkey Business ohne Entspannung
    """
    return solve(lines, UpsetMonkey, 10000)


def solve(lines, cls, rounds):
    """
    Generierung einer Liste von Affen der richtigen Art
    Durchführung der Runden
    Lösung ist das Produkt der beiden höchsten Inspektionswerte
    """
    monkeys = convert(lines, cls)
    for _ in range(rounds):
        do_monkey_business_round(monkeys)
    counts = sorted(map(lambda monkey: monkey.count, monkeys))
    return counts[-2] * counts[-1]


class Monkey:
    """
    Monkey-Klasse für Part 1
    """

    def __init__(self, lines):
        """
        Parsen der Input-Zeilen
        Initialisierung der Attribute
        - num        : Nummer des Affen
        - items      : Gegenstände bzw. Level beim Affen
        - operation  : Formel zur Berechnung des Folgelevels
        - divisor    : Divisor für den Resttest
        - true_test  : Affennummer, zu dem das Item geworfen wird, falls kein Rest
        - false_test : Affennummer, zu dem das Item geworfen wird, falls Rest vorhanden
        - count      : Anzahl der Inspektionen, die der Affe bereits ausgeführt hat
        """
        if len(lines) != 6:
            raise Exception("Lines count wrong")
        m = re.search(r"^Monkey (\d+):$", lines[0].strip())
        self.num = int(m.group(1))
        m = re.search(r"Starting items:(.+)$", lines[1].strip())
        self.items = list(map(int, m.group(1).split(",")))
        m = re.search(r"Operation:(.+)$", lines[2].strip())
        self.operation = m.group(1).strip()
        m = re.search(r"Test: divisible by (\d+)$", lines[3].strip())
        self.divisor = int(m.group(1))
        m = re.search(r"If true: throw to monkey (\d+)$", lines[4].strip())
        self.true_dest = int(m.group(1))
        m = re.search(r"If false: throw to monkey (\d+)$", lines[5].strip())
        self.false_dest = int(m.group(1))
        if self.true_dest == self.num or self.false_dest == self.num:
            raise Exception("Throwing to myself")
        self.count = 0

    def do_business(self, monkeys):
        """
        Durchführung des Monkey Business für einen Affen
        Jedes Item wird untersucht, das Level neu berechnet und
        in Abhängigkeit davon zum nächsten Affen geworfen
        """
        while len(self.items) > 0:
            item = self.items.pop(0)
            self.count += 1 # one more inspection
            item = self.calc_new_level(item)
            if item % self.divisor == 0:
                monkeys[self.true_dest].items.append(item)
            else:
                monkeys[self.false_dest].items.append(item)

    def calc_new_level(self, item):
        """
        Berechnug des neuen Level
        Ausführen der eingelesenen Formel
        Teilen des Levels durch 3
        """
        loc = {'old': item}
        exec(self.operation, globals(), loc)
        return loc['new'] // 3


class UpsetMonkey(Monkey):
    """
    Monkey-Klasse für Part 2
    Es entfällt das Teilen des Levels durch 3, wodurch die Levelwerte stark
    ansteigen würden (und damit die Laufzeit). Die Idee ist, die Level durch eine
    Modulo-Rechnung zu begrenzen, ohne dass die Resteprüfungen davon beeinflusst werden.
    Lösung: wir rechnen im Modul des Produkts aller Divisoren für die Resteprüfung
    Noch besser wäre das KGV aller Divisoren, aber da die Divisoren in den Beispielen
    immer prim sind, ist das Produkt das KGV
    """

    divisors = []       # Klassenvariable, in der alle Divisoren gesammelt werden
    modul = None

    def __init__(self, lines):
        """
        Konstruktor, der neben der Initialisierung der Attribute auch den Divisor vermerkt
        """
        super().__init__(lines)
        UpsetMonkey.divisors.append(self.divisor)

    def calc_new_level(self, item):
        """
        Angepasste Neuberechnung des Levels im Modul des Produkts aller Divisoren
        """
        loc = {'old': item}
        exec(self.operation, globals(), loc)
        return loc['new'] % UpsetMonkey.get_modul()

    @classmethod
    def get_modul(cls):
        """
        Ermitteln des Produkts aller Teiler der Affen
        """
        if UpsetMonkey.modul is None:
            UpsetMonkey.modul = reduce(lambda acc, val: acc*val, UpsetMonkey.divisors)
        return UpsetMonkey.modul


def convert(lines: List[str], cls = Monkey) -> List[Monkey]:
    """
    Umwandlung der Inputzeilen in eine Liste von Affen
    Die zu verwendende Affen-Klasse wird injected
    """
    return list(map(lambda line_chunks: cls(line_chunks), next_n_lines(lines, 6)))


def next_n_lines(lines, n):
    """
    Generator für das blockweise Einlesen der Eingabezeilen
    Gelesen werden immer n Zeilen und dann eine Leerzeile übersprungen
    """
    for i in range(0, len(lines), n + 1):
        yield lines[i:i + n]


def do_monkey_business_round(monkeys):
    """
    Eine Runde Monkey Business
    """
    for monkey in monkeys:
        monkey.do_business(monkeys)


if __name__ == '__main__':
    lines = read_puzzle("data/day11.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

