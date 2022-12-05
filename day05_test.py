from day05 import split_lines, stack_lines_to_stacks,  movement_lines_to_tuple, do_movement, top_line, solve01, solve02


def data():
    return [
        "    [D]    \n",
        "[N] [C]    \n",
        "[Z] [M] [P]\n",
        " 1   2   3 \n",
        "\n",
        "move 1 from 2 to 1\n",
        "move 3 from 1 to 3\n",
        "move 2 from 2 to 1\n",
        "move 1 from 1 to 2\n"]


def test_split_lines():
    lines = data()
    stacks, movements = split_lines(lines)
    assert len(stacks) == 4
    assert len(movements) == 4


def test_stack_lines():
    lines = data()
    stack_lines, _ = split_lines(lines)
    stacks = stack_lines_to_stacks(stack_lines)
    assert stacks[1].pop() == 'N'
    assert len(stacks[2]) == 3


def test_movement():
    lines = data()
    stack_lines, movements_lines = split_lines(lines)
    stacks = stack_lines_to_stacks(stack_lines)
    movement_tuples = movement_lines_to_tuple(movements_lines)
    do_movement(stacks, movement_tuples[0])
    assert stacks[1][-1] == 'D'


def test_top_line():
    lines = data()
    stack_lines, _ = split_lines(lines)
    stacks = stack_lines_to_stacks(stack_lines)
    result = top_line(stacks)
    assert result == 'NDP'


def test_solve1():
    lines = data()
    result = solve01(lines)
    assert result == "CMZ"

def test_solve2():
    lines = data()
    result = solve02(lines)
    assert result == "MCD"
