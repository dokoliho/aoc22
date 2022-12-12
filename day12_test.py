from typing import List
from day12 import solve01, solve02, convert_to_height_matrix, create_edges, dijkstra, Node


def data() -> List[str]:
    return [
        "Sabqponm\n",
        "abcryxxl\n",
        "accszExk\n",
        "acctuvwj\n",
        "abdefghi\n",
     ]


def test_convert_to_matrix():
    lines = data()
    matrix = convert_to_height_matrix(lines)
    source = Node.source_node
    destination = Node.destination_node
    assert len(matrix) == 5
    assert len(matrix[0]) == 8
    assert source.row == 0
    assert source.col == 0
    assert source.height == 0
    assert destination.row == 2
    assert destination.col == 5
    assert destination.height == 25


def test_create_edges():
    lines = data()
    matrix = convert_to_height_matrix(lines)
    edges = create_edges(matrix)
    assert edges[0].source.row == 0
    assert edges[0].source.col == 0
    assert edges[0].destination.row == 1
    assert edges[0].destination.col == 0


def test_dijkstra():
    lines = data()
    matrix = convert_to_height_matrix(lines)
    edges = create_edges(matrix)
    assert dijkstra(Node.source_node, Node.destination_node, edges) == 31


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 31


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 29
