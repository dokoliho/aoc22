from typing import List
from day21 import solve01, solve02, convert, Monkey


def data() -> List[str]:
    return [
        'root: pppw + sjmn\n',
        'dbpl: 5\n',
        'cczh: sllz + lgvd\n',
        'zczc: 2\n',
        'ptdq: humn - dvpt\n',
        'dvpt: 3\n',
        'lfqf: 4\n',
        'humn: 5\n',
        'ljgn: 2\n',
        'sjmn: drzm * dbpl\n',
        'sllz: 4\n',
        'pppw: cczh / lfqf\n',
        'lgvd: ljgn * ptdq\n',
        'drzm: hmdt - zczc\n',
        'hmdt: 32\n',
    ]


def test_convert():
    lines = data()
    monkeys = convert(lines)
    assert len(monkeys) == 15
    assert monkeys['hmdt'].dependencies == []
    assert monkeys['hmdt'].value == 32
    assert monkeys['cczh'].dependencies == ['sllz', 'lgvd']
    assert monkeys['cczh'].value == 'sllz + lgvd'


def test_get_value():
    lines = data()
    monkeys = convert(lines)
    assert monkeys['hmdt'].get_value(monkeys) == 32
    assert monkeys['zczc'].get_value(monkeys) == 2
    assert monkeys['drzm'].get_value(monkeys) == 30


def test_has_human_dependency():
    lines = data()
    monkeys = convert(lines)
    assert monkeys['hmdt'].has_human_dependency(monkeys) is False
    assert monkeys['humn'].has_human_dependency(monkeys) is True
    assert monkeys['ptdq'].has_human_dependency(monkeys) is True
    assert monkeys['drzm'].has_human_dependency(monkeys) is False


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 152


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 301


