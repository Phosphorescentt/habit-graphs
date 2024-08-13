"""
habits:
habit 0
habit 1
habit 2
dependencies:
0,2,10
1,2,4
2,0,0
2,1,4
"""

import sys

from processes import (
    build_habit_graph,
    order_habit_graph,
    read_habit_graph,
    write_habit_graph,
)


def main(proc_name: str):
    match proc_name:
        case "gen":
            # generate a habit file
            filename = input("(filename) ")
            assert filename.endswith(".hg")
            hg = build_habit_graph()
            write_habit_graph(filename, hg)
            raise NotImplementedError
        case "ord":
            # order a habit file
            filename = input("(filename) ")
            assert filename.endswith(".hg")
            hg = read_habit_graph(filename)
            ordered_habits = order_habit_graph(hg)
            for habit in ordered_habits:
                print(habit)
        case _:
            pass
            raise NotImplementedError


if __name__ == "__main__":
    main(sys.argv[1])
