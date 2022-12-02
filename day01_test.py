from day01 import solve


def test_solve():
    puzzle = ["1000\n", "2000\n",  "3000\n", "\n",
              "4000\n", "\n",
              "5000\n", "6000\n", "\n",
              "7000\n", "8000\n", "9000\n", "\n",
              "10000\n",  "\n"]
    assert solve(puzzle) == 45000

