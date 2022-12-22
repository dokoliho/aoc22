from typing import List
from day22 import solve01, solve02, convert, Maze, Direction


def data() -> List[str]:
    return [
        '        ...#\n',
        '        .#..\n',
        '        #...\n',
        '        ....\n',
        '...#.......#\n',
        '........#...\n',
        '..#....#....\n',
        '..........#.\n',
        '        ...#....\n',
        '        .....#..\n',
        '        .#......\n',
        '        ......#.\n',
        '\n',
        '10R5L5R10L4R5L5\n',
    ]


def test_convert():
    lines = data()
    maze, command = convert(lines)
    assert command == [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5]
    assert len(maze.lines) == 12


def test_start_pos():
    lines = data()
    maze, command = convert(lines)
    row, col = maze.start_position()
    assert row == 0
    assert col == 8

def test_move_one_pos():
    lines = data()
    maze, command = convert(lines)
    position = maze.start_position()
    direction = Direction(0)
    (row, col), cont = maze.move_one_step(position, direction)
    assert row == 0
    assert col == 9
    assert cont is True
    position = (0, 9)
    direction = Direction(1)
    (row, col), cont = maze.move_one_step(position, direction)
    assert row == 0
    assert col == 9
    assert cont is False
    position = (1, 11)
    direction = Direction(0)
    (row, col), cont = maze.move_one_step(position, direction)
    assert row == 1
    assert col == 8
    assert cont is True


def test_move_path():
    lines = data()
    maze, path = convert(lines)
    position = maze.start_position()
    direction = Direction(0)
    (row, col), end_direction = maze.move_path(position, direction, path)
    assert row == 5
    assert col == 7
    assert end_direction.facing == 0




def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 6032


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0


