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
    # class variables
    max_energy: int = 50
    start_loc = "intro"
    quit_loc = "quit"
    lose_loc = "lose"

    # instance vars
    def __init__(self, terminal_width: int) -> None:
        self.works: list[Artwork] = []
        self.energy_level: int = random.randint(10, 35)
        self.crit_energy: int = random.randint(56, 70)
        self.win_value: int = random.randint(100, 500)
        self.location: str = self.start_loc
        self.prev_location: str | None = None
        self.quit_location: str = self.quit_loc
        self.delay: int = 5
        self.terminal_width: int = terminal_width
        self.status_reason = None

    def won_by_value(self) -> bool:
        if self.works:
            total_value = sum(work.value for work in self.works)
            if total_value >= self.win_value:
                return True
        return False

    def move(self, new_location) -> None:
        self.prev_location = self.location
        self.location = new_location

    def quit(self) -> None:
        self.move(self.quit_loc)

    def lose(self, reason) -> None:
        self.status_reason = reason
        self.move(self.lose_loc)

    def drink_coffee(self) -> None:
        self.energy_level += random.randint(5, 20)
