from typing import List
from day07 import solve01, solve02, build_tree, print_tree


def data() -> List[str]:
    return [
        "$ cd /\n",
        "$ ls\n",
        "dir a\n",
        "14848514 b.txt\n",
        "8504156 c.dat\n",
        "dir d\n",
        "$ cd a\n",
        "$ ls\n",
        "dir e\n",
        "29116 f\n",
        "2557 g\n",
        "62596 h.lst\n",
        "$ cd e\n",
        "$ ls\n",
        "584 i\n",
        "$ cd..\n",
        "$ cd..\n",
        "$ cd d\n",
        "$ ls\n",
        "4060174 j\n",
        "8033020 d.log\n",
        "5626152 d.ext\n",
        "7214296 k\n"
    ]

def test_build_tree():
    lines: List[str] = data()
    tree = build_tree(lines)
    print_tree(tree)



def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 95437


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 24933642
