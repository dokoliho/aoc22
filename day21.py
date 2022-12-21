from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


class Monkey:
    """
    Repräsentation für einen Affen
    Attribute:
    - has_human_dep     Hängt der Wert vom Menschen ab? True/False/None (=ungeklärt)
    - name              Name des Affen
    - dependencies      Liste der Affennamen, von denen der Affe abhängig ist
    - value             Integer-Wert oder Formel
    - operation         Ein Zeichen + - * /
    """
    def __init__(self, line):
        """
        Konstruktor
        """
        self.has_human_dep = None
        tokens = line.strip().split(":")
        self.name = tokens[0].strip()
        m = re.search(r"^(-?\d+)$", tokens[1].strip())
        if m:
            self.dependencies = []
            self.value = int(m.group(1))
            self.operation = None
            self.has_human_dep = True if self.name == 'humn' else False
            return
        m = re.search(r"^([a-z]{4}) ([+\-*/]) ([a-z]{4})$", tokens[1].strip())
        if m:
            self.dependencies = [m.group(1), m.group(3)]
            self.value = tokens[1].strip()
            self.operation = m.group(2)
            return
        raise Exception(f"Syntax Error: {line}")

    def get_value(self, all_monkeys):
        """
        Berechnung des Werts (sofern noch nicht erfolgt)
        """
        if not isinstance(self.value, int):
            loc = {}
            for name in self.dependencies:
                loc[name] = all_monkeys[name].get_value(all_monkeys)
            exec(f"result = {self.value}", globals(), loc)
            self.value = int(loc['result'])
        return self.value

    def has_human_dependency(self, all_monkeys):
        """
        Berechnung der Abhängigkeit vom Menschen (sofern noch nicht erfolgt)
        """
        if self.has_human_dep is None:
            m0 = all_monkeys[self.dependencies[0]]
            m1 = all_monkeys[self.dependencies[1]]
            self.has_human_dep = m0.has_human_dependency(all_monkeys) or m1.has_human_dependency(all_monkeys)
        return self.has_human_dep

    def adjust_human(self, all_monkeys, expected_value=None):
        """
        Berechnung der Anpassung
        Voraussetzung: Abhängigkeit vom Menschen
        Rekursiver Abstieg im Berechnungsbaum bis zum Menschen
        Dort Rekursionsabbruch
        """
        if not self.has_human_dependency(all_monkeys):
            raise Exception(f"{self.name}: Nothing to adjust")
        if self.name == 'humn':
            print(f"I have to yell {expected_value}")
            return expected_value
        m0 = all_monkeys[self.dependencies[0]]
        m1 = all_monkeys[self.dependencies[1]]
        if self.name == 'root':
            if m0.has_human_dependency(all_monkeys):
                return m0.adjust_human(all_monkeys, m1.get_value(all_monkeys))
            else:
                return m1.adjust_human(all_monkeys, m0.get_value(all_monkeys))
        if self.operation == '+':
            if m0.has_human_dependency(all_monkeys):
                return m0.adjust_human(all_monkeys, expected_value - m1.get_value(all_monkeys))
            else:
                return m1.adjust_human(all_monkeys, expected_value - m0.get_value(all_monkeys))
        if self.operation == '-':
            if m0.has_human_dependency(all_monkeys):
                return m0.adjust_human(all_monkeys, expected_value + m1.get_value(all_monkeys))
            else:
                return m1.adjust_human(all_monkeys, m0.get_value(all_monkeys) - expected_value)
        if self.operation == '*':
            if m0.has_human_dependency(all_monkeys):
                return m0.adjust_human(all_monkeys, expected_value // m1.get_value(all_monkeys))
            else:
                return m1.adjust_human(all_monkeys, expected_value // m0.get_value(all_monkeys))
        if self.operation == '/':
            if m0.has_human_dependency(all_monkeys):
                return m0.adjust_human(all_monkeys, expected_value * m1.get_value(all_monkeys))
            else:
                return m1.adjust_human(all_monkeys, m0.get_value(all_monkeys) // expected_value)


def solve01(lines: List[str]) -> int:
    """
    Berechnung des Werts von root
    """
    monkeys = convert(lines)
    return monkeys['root'].get_value(monkeys)


def solve02(lines: List[str]) -> int:
    """
    Berechnung des Werts von humn, so dass gleiche Werte bei root auflaufen
    """
    monkeys = convert(lines)
    return monkeys['root'].adjust_human(monkeys)


def convert(lines):
    """
    Konvertieren der Eingabezeilen in ein Monkey-Dictionary
    """
    monkey_list = map(lambda line: Monkey(line), lines)
    return {m.name: m for m in monkey_list}


if __name__ == '__main__':
    lines = read_puzzle("data/day21.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
