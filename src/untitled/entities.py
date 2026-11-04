# untitled entities

from enum import Enum
import random

class ArtType(Enum):
    PAINTING = 'painting'
    DRAWING = 'drawing'
    # can add more

class Artwork:
    def __init__(self) -> None:
        self.type: ArtType = random.choice(list(ArtType)).lower()
        self.value: int = random.randint(1, 20)

    def __eq__(self, other):
        if isinstance(other, Artwork):
            if (self.type == other.type and
                self.value is other.value):
                return True
        return False

class Player:
    def __init__(self, start_node: str, quit_node: str, terminal_width: int) -> None:
        self.works[Artwork] = []
        self.energy_level: int = random.randint(10, 35)
        self.max_energy: int = 50
        self.crit_energy: int = random.randint(55, 70)
        self.win_value: int = random.randint(100, 500)
        self.current_node: str = start_node
        self.prev_node: str | None = None
        self.quit_node: str = quit_node
        self.delay: int = 5
        self.terminal_width: int = terminal_width

    def won_by_value(self) -> bool:
        if self.works:
            total_value = sum(work.value for work in self.works)
            if total_value >= self.win_value:
                return True
        return False
