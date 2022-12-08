from typing import List
from day08 import solve01, solve02, convert_to_array, count_external_visible_trees_of_one_line, transpose_matrix, height


def data() -> List[str]:
    return [
        "30373\n",
        "25512\n",
        "65332\n",
        "33549\n",
        "35390\n",
    ]


def test_convert():
    lines = data()
    m = convert_to_array(lines)
    assert len(m) == 5
    assert len(m[0]) == 5


def test_count_visible_trees():
    lines = data()
    m = convert_to_array(lines)
    trees = m[0]
    count, trees = count_external_visible_trees_of_one_line(trees)
    assert count == (2 + 1)


def test_transpose():
    lines = data()
    m = convert_to_array(lines)
    m = transpose_matrix(m)
    assert len(m) == 5
    assert len(m[0]) == 5
    assert height(m[0][1]) == 2


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 21


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 8
