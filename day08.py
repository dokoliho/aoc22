import operator
from functools import reduce
from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Ermitteln der von außen sichtbaren Bäume
    Dazu wird zuerst die horizontale Blickrichtung benutzt,
    anschließend die Matrix transponiert und erneut
    horizontal betrachtet
    """
    tree_matrix = convert_to_array(lines)
    row_sum, new_matrix = count_external_visible_trees_of_matrix_by_line(tree_matrix)
    col_sum, _ = count_external_visible_trees_of_matrix_by_line(transpose_matrix(new_matrix))
    return row_sum + col_sum


def solve02(lines: List[str]) -> int:
    """
    Ermitteln des besten "Sceneic Score"
    """
    tree_matrix = convert_to_array(lines)
    return max(scenic_scores(tree_matrix))


def convert_to_array(lines):
    """
    Umwandeln der vorgegebenen Baumhöhenstrings in ein zweidimensionales Array von Tupeln,
    in denen der erste Wert die Höhe und der zweite Wert die Tatsache wiedergibt, ob der
    Baum bereits von außen gesehen wurde.
    ['30373\n', '25512\n', '65332\n', '33549\n', '35390\n'] ->
    [[(3, False), (0, False), (3, False), (7, False), (3, False)],
     [(2, False), (5, False), (5, False), (1, False), (2, False)],
     [(6, False), (5, False), (3, False), (3, False), (2, False)],
     [(3, False), (3, False), (5, False), (4, False), (9, False)],
     [(3, False), (5, False), (3, False), (9, False), (0, False)]]
    """
    result = reduce(lambda acc, l: acc + [(convert_to_list_of_tuples(l))], lines, list())
    return result


def convert_to_list_of_tuples(line):
    """
    Umwandlung einer Zeile
    '30373\n' ->
    [(3, False), (0, False), (3, False), (7, False), (3, False)]
    """
    return list(map(lambda el: (int(el), False),  list(line.strip())))


def count_external_visible_trees_of_matrix_by_line(tree_matrix):
    """
    Ermitteln der aus horizontaler Blickrichtung
    von außen sichtbaren Bäume eines Waldes.
    Zurückgegeben wird eine neue Matrix, in der
    die bereits gesichteten Bäume markiert sind
    """
    sum = 0
    new_tree_matrix = []
    for row in tree_matrix:
        count, trees = count_external_visible_trees_of_one_line(row)
        sum += count
        new_tree_matrix.append(trees)
    return sum, new_tree_matrix


def count_external_visible_trees_of_one_line(trees):
    """
    Ermitteln der aus horizontaler Blickrichtung
    von außen sichtbaren Bäume einer Baumzeile.
    Zurückgegeben wird eine neue Zeile, in der
    die bereits gesichteten Bäume markiert sind
    """
    from_left_count, new_trees = count_external_visible_trees_from_left(trees)
    from_right_count, new_trees = count_external_visible_trees_from_left(reversed(new_trees))
    new_trees.reverse()
    return from_left_count+ from_right_count, new_trees


def count_external_visible_trees_from_left(trees, blocking=-1):
    """
    Ermitteln der "von links"
    von außen sichtbaren Bäume einer Baumzeile.
    Zurückgegeben wird eine neue Zeile, in der
    die bereits gesichteten Bäume markiert sind
    """
    count = 0
    new_trees = []
    for tree in trees:
        if height(tree) > blocking and not(seen(tree)):
            count += 1
            new_trees.append((height(tree), True))
        else:
            new_trees.append(tree)
        blocking = max(height(tree), blocking)
    return count, new_trees


def scenic_scores(tree_matrix):
    """
    Iterator, der die Scores aller Bäume liefert
    """
    transpose = transpose_matrix(tree_matrix)
    for row in range(len(tree_matrix)):
        for col in range(len(transpose)):
            tree = tree_matrix[row][col]
            views = [
                tree_matrix[row][col + 1:],         # right
                reversed(tree_matrix[row][:col]),   # left
                transpose[col][row + 1:],           # down
                reversed(transpose[col][:row])      # up
            ]
            yield reduce(operator.mul, map(lambda l: count_visible_from_tree_with_height(l, height(tree)), views), 1)


def count_visible_from_tree_with_height(trees, tree_height=100):
    """
    Zählt die Bäume in der übergebenen Linie, bis
    die Sichtlinie durch einen gleich hohen oder höheren Baum
    unterbrochen wird
    """
    count = 0
    for tree in trees:
        count += 1
        if height(tree) >= tree_height:
            break
    return count


def height(tree):
    return tree[0]


def seen(tree):
    return tree[1]


def transpose_matrix(matrix):
    """
    Transponieren der Matrix
    """
    transpose = [[] for _ in range(len(matrix[0]))]
    for row in matrix:
        for index, element in enumerate(row):
            transpose[index].append(element)
    return transpose


if __name__ == '__main__':
    lines = read_puzzle("data/day8.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

