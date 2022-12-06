from day06 import  solve01, solve02


def prepare_data(s):
    return [s]



def test_solve1():
    lines = prepare_data("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    assert 7 == solve01(lines)
    lines = prepare_data("bvwbjplbgvbhsrlpgdmjqwftvncz")
    assert 5 == solve01(lines)
    lines = prepare_data("nppdvjthqldpwncqszvftbrmjlhg")
    assert 6 == solve01(lines)
    lines = prepare_data("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    assert 10 == solve01(lines)
    lines = prepare_data("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    assert 11 == solve01(lines)

def test_solve2():
    lines = prepare_data("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    assert 19 == solve02(lines)
    lines = prepare_data("bvwbjplbgvbhsrlpgdmjqwftvncz")
    assert 23 == solve02(lines)
    lines = prepare_data("nppdvjthqldpwncqszvftbrmjlhg")
    assert 23 == solve02(lines)
    lines = prepare_data("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    assert 29 == solve02(lines)
    lines = prepare_data("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    assert 26 == solve02(lines)