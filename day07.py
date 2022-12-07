from functools import reduce
from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Ermitteln aller Dir-Größen
    Addieren der Verzeichnisse mit einer Größe <= 100000
    """
    tree = build_tree(lines)
    sizes = map(lambda tup: tup[1], dir_names_with_sizes("/", tree))
    return sum(filter(lambda value: value <= 100000, sizes))


def solve02(lines: List[str]) -> int:
    """
    Ermitteln des kleinsten Verzeichnisses, nach dessen Löschung
    Ausreichend Platz für das Update verbleibt
    """
    tree = build_tree(lines)
    names_with_sizes = dir_names_with_sizes("/", tree)
    total_used = next(size for name, size in names_with_sizes if name == '/')
    free_space = 70000000 - total_used
    needed = 30000000 - free_space
    sizes = map(lambda tup: tup[1], names_with_sizes)
    big_enough_sizes = sorted(list(filter(lambda size: size >= needed, sizes)))
    return big_enough_sizes[0]


def build_tree(lines):
    """
    Aufbau von verschachtelten Dictionaries, die die Verzeichnisstruktur wiedergeben
    Key eines Dictionary-Eintrags ist der Dateiname, der Verzeichnisname oder ".."
    Value des Dictionary-Eintrags ist die Dateigröße, ein weiters Verzeichnisdictionary oder das übergeordnete Dict.
    """
    tree = {'..': None}  # root hat kein übergeordnetes Verzeichnis
    working_dir = tree
    for line in lines:
        working_dir = process_line(line.strip(), tree, working_dir)
    return tree


def process_line(line, tree, working_dir):
    """
    Unterscheidung Befehlszeile oder Ausgabezeile
    Der tree wird "in situ" aktualisiert
    Das neue Working-Directory wird zurückgegeben
    """
    if line.startswith("$"):
        return process_command(line, tree, working_dir)
    else:
        process_output(line, working_dir)
        return working_dir


def process_command(line, tree, working_dir):
    """
    Auswertung einer Befehlszeile
    Einzige relevante Auswirkung ist die Änderung des
    Working Directories
    """
    m = re.search(r"cd(.+)$", line)
    if m:
        arg = m.group(1).strip()
        if arg == "/":
            return tree
        return working_dir[arg]
    return working_dir


def process_output(line, working_dir):
    """
    Verarbeitung einer Ausgabezeile
    Die Informationen werden im Working Directory vermerkt
    Neue Unterverzeichnisse werden leer angelegt und mit dem Elternverzeichnis verknüpft
    """
    s1, s2 = tuple(line.split(" "))
    if s1 == "dir":
        if not s2 in working_dir:
            working_dir[s2] = {'..': working_dir}
    else:
        working_dir[s2] = int(s1)


def print_tree(tree):
    """
    Ausgabe des gesamten Baums auf der Konsole
    """
    print()
    print("- /")
    print_branch(tree, 1)


def print_branch(branch, indent=1):
    """
    Ausgabe des Teilbaums auf der Konsole
    """
    for key, element in all_dir_entries(branch):
        if type(element) is dict:
            print("  " * indent + "- " + key + " (dir)")
            print_branch(element, indent+1)
        else:
            print("  " * indent + "- " + key + " " + str(element))


def size_branch(branch):
    """
    Ermitteln der Größe eines Zweigs im Verzeichnisbaum
    """
    values = map(lambda tup: tup[1], all_dir_entries(branch))
    return reduce(lambda acc, elm: acc + (size_branch(elm) if type(elm) is dict else elm), values, 0)


def dir_names_with_sizes(name, branch):
    """
    Generierung einer Liste von Tupeln ("Vezeichnisname", Größe)
    innerhalb des übergebenen Branch
    Der übergebene Branch selbst ist auch in der Liste enthalten;
    sein Name wird ebenfalls übergeben
    """
    return reduce(lambda acc, elm: acc + dir_names_with_sizes(elm[0], elm[1]),
                  all_subdirs(branch),
                  [(name, size_branch(branch))])


def all_subdirs(branch):
    """
    Iterator über alle Unterverzeichnisse eines Verzeichnisses
    """
    for key, element in all_dir_entries(branch):
        if type(element) is dict:
            yield key, element


def all_dir_entries(branch):
    """
    Iterator über alle Einträge eines Verzeichnisses
    """
    for key, element in branch.items():
        if key == '..':
            continue
        yield key, element


if __name__ == '__main__':
    lines = read_puzzle("data/day7.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

