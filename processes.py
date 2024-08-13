import networkx as nx

from typing import List
from models import Dependency, DependencyStore, Habit, HabitGraph


def build_habit_graph() -> HabitGraph:
    in_str = ""
    habit_names = []
    while True:
        in_str = input("(habit name) ")
        if in_str == "c":
            break

        habit_names.append(in_str)

    in_str = ""
    deps = []
    while True:
        in_str = input("(dependency) ")
        if in_str == "c":
            break

        deps.append(in_str.split(","))

    hg = HabitGraph.new()
    hg.habits.update({i: Habit(id=i, name=name) for i, name in enumerate(habit_names)})
    for dep in deps:
        dependency = Dependency(dependee_id=dep[0], dependant_id=dep[1])
        hg.dependency_store.add_dependency(dependency, dep[2])

    return hg


def write_habit_graph(filename: str, hg: HabitGraph) -> bool:
    lines = ["habits:\n"]
    lines.extend([habit.name + "\n" for habit in hg.habits.values()])
    lines.append("dependencies:\n")
    lines.extend([",".join(dep) + "\n" for dep in hg.dependency_store.as_tuples_str()])

    with open(filename, "w") as f:
        f.writelines(lines)

    return True


def read_habit_graph(filename: str) -> HabitGraph:
    hg = HabitGraph(habits={}, dependency_store=DependencyStore(dependency_map={}))
    reading_habits = False
    reading_dependencies = False
    with open(filename, "r") as f:
        for line in f.readlines():
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


def order_habit_graph(hg: HabitGraph) -> List[Habit]:
    G = nx.DiGraph()
    G.add_nodes_from([habit.id for habit in hg.habits.values()])
    G.add_weighted_edges_from(hg.dependency_store.as_tuples())

    habit_ids = list(nx.topological_sort(G))
    ordered_habits = [hg.habits[id] for id in habit_ids]

    return ordered_habits
