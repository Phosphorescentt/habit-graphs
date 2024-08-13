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
from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Tuple

import networkx as nx


@dataclass
class Habit:
    id: int
    name: str


class Dependency(NamedTuple):
    dependee_id: int
    dependant_id: int

    def reversed(self):
        return Dependency(dependee_id=self.dependant_id, dependant_id=self.dependee_id)


@dataclass
class DependencyStore:
    dependency_map: Dict[Dependency, int]

    def add_dependency(self, d: Dependency, strength: int):
        if existing_strength := self.dependency_map.get(d.reversed()):
            if strength > existing_strength:
                # remove old connection as this new one takes priority
                self.dependency_map[d] = strength
                del self.dependency_map[d.reversed()]
        else:
            self.dependency_map[d] = strength

    def as_tuples(self) -> List[Tuple[int, int, int]]:
        return [
            (k.dependee_id, k.dependant_id, v) for k, v in self.dependency_map.items()
        ]


@dataclass
class HabitGraph:
    habits: Dict[int, Habit]
    dependency_store: DependencyStore


def read_habit_graph(filename: str) -> HabitGraph:
    hg = HabitGraph(habits={}, dependency_store=DependencyStore(dependency_map={}))
    reading_habits = False
    reading_dependencies = False
    with open(filename, "r") as f:
        for line in f.readlines():
            print(line)
            if line.startswith("habits:") and not reading_habits:
                reading_habits = True
                reading_dependencies = False
                continue

            if line.startswith("dependencies:") and not reading_dependencies:
                reading_dependencies = True
                reading_habits = False
                continue

            if reading_habits:
                hg.habits[len(hg.habits)] = Habit(id=len(hg.habits), name=line)

            if reading_dependencies:
                dependee_id, dependant_id, strength = line.split(",")
                hg.dependency_store.add_dependency(
                    d=Dependency(
                        dependee_id=int(dependee_id),
                        dependant_id=int(dependant_id),
                    ),
                    strength=int(strength),
                )

    return hg


def order(hg: HabitGraph) -> List[Habit]:
    G = nx.DiGraph()
    G.add_nodes_from([habit.id for habit in hg.habits.values()])
    G.add_weighted_edges_from(hg.dependency_store.as_tuples())

    habit_ids = list(nx.topological_sort(G))
    ordered_habits = [hg.habits[id] for id in habit_ids]

    return ordered_habits


def build_graph(filename: str) -> HabitGraph:
    pass


def main(proc_name: str):
    match proc_name:
        case "gen":
            # generate a habit file
            filename = input("(filename) ")
            assert filename.endswith(".hg")
        case "ord":
            # order a habit file
            filename = input("(filename) ")
            assert filename.endswith(".hg")
            hg = read_habit_graph(filename)
            print(order(hg))
        case _:
            pass


if __name__ == "__main__":
    main(sys.argv[1])
