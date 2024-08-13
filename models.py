from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Tuple


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
        """Add a new dependency to the store's dependency map.

        We can't just add every dependency to the graph as otherwise we end up
        with a complete graph which is ALL cycles and thus we can't apply
        any sorting to it easily.
        """
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

    def as_tuples_str(self) -> List[Tuple[str, str, str]]:
        return [
            (str(k.dependee_id), str(k.dependant_id), str(v))
            for k, v in self.dependency_map.items()
        ]


@dataclass
class HabitGraph:
    habits: Dict[int, Habit]
    dependency_store: DependencyStore

    @staticmethod
    def new():
        return HabitGraph(
            habits={},
            dependency_store=DependencyStore(
                dependency_map={},
            ),
        )
