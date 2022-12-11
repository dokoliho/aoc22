from typing import List
from day11 import solve01, solve02, convert, Monkey


def data() -> List[str]:
    return [
        'Monkey 0:\n',
        '  Starting items: 79, 98\n',
        '  Operation: new = old * 19\n',
        '  Test: divisible by 23\n',
        '    If true: throw to monkey 2\n',
        '    If false: throw to monkey 3\n',
        '\n',
        'Monkey 1:\n',
        '  Starting items: 54, 65, 75, 74\n',
        '  Operation: new = old + 6\n',
        '  Test: divisible by 19\n',
        '    If true: throw to monkey 2\n',
        '    If false: throw to monkey 0\n',
        '\n',
        'Monkey 2:\n',
        '  Starting items: 79, 60, 97\n',
        '  Operation: new = old * old\n',
        '  Test: divisible by 13\n',
        '    If true: throw to monkey 1\n',
        '    If false: throw to monkey 3\n',
        '\n',
        'Monkey 3:\n',
        '  Starting items: 74\n',
        '  Operation: new = old + 3\n',
        '  Test: divisible by 17\n',
        '    If true: throw to monkey 0\n',
        '    If false: throw to monkey 1\n',
     ]


def test_convert():
    lines = data()
    monkeys = convert(lines)

    assert len(monkeys) == 4

    assert monkeys[0].num == 0
    assert monkeys[0].items == [79, 98]
    assert monkeys[0].operation == "new = old * 19"
    assert monkeys[0].divisor == 23
    assert monkeys[0].true_dest == 2
    assert monkeys[0].false_dest == 3

    assert monkeys[1].num == 1
    assert monkeys[1].items == [54, 65, 75, 74]
    assert monkeys[1].operation == "new = old + 6"
    assert monkeys[1].divisor == 19
    assert monkeys[1].true_dest == 2
    assert monkeys[1].false_dest == 0


def test_do_business():
    lines = data()
    monkeys = convert(lines)
    monkeys[0].do_business(monkeys)
    assert monkeys[0].count == 2
    assert monkeys[0].items == []
    assert monkeys[3].items == [74, 500, 620]



def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
