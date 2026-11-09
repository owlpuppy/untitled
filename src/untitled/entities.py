# untitled entities

import shutil, random
from enum import Enum

class ArtType(Enum):
    PAINTING = 'painting'
    DRAWING = 'drawing'
    # can add more

class PlayerMood(Enum):
    GRRR = "grrr", -5
    BLEGH = "blegh", -2
    OKI = "oki", 0
    COLON_THREE = ":3", 2
    UWU = "uwu", 5

class Artwork:
    def __init__(self, liked: PlayerMood) -> None:
        self.type: ArtType = random.choice(list(ArtType)).value
        self.value: int = random.randint(1, 20)
        self.liked: PlayerMood = liked

    def __eq__(self, other):
        if isinstance(other, Artwork):
            if (self.type == other.type and
                self.value is other.value and
                self.liked is other.liked):
                return True
        return False

class Player:
    # class variables
    max_energy: int = 50
    start_loc = "intro"
    quit_loc = "quit"
    lose_loc = "lose"
    setup_loc = "setup"
    mood_list = list(PlayerMood)

    # instance vars
    def __init__(self) -> None:
        self.works: list[Artwork] = []
        self.energy: int = random.randint(10, 35)
        self.mood: PlayerMood = PlayerMood.OKI
        self.studio_time = 0
        self.crit_energy: int = random.randint(60, 75)
        self.win_value: int = random.randint(100, 500)
        self.location: str = self.start_loc
        self.prev_location: str | None = None
        self.delay: int = 5
        self.terminal_width: int = shutil.get_terminal_size().columns
        self.status_reason = None

    # mechanic instance methods

    def won_by_value(self) -> bool:
        if self.works:
            total_value = sum(work.value for work in self.works)
            if total_value >= self.win_value:
                return True
        return False

    def get_mood_range(self) -> tuple[int, int, int]:
        return 0, len(self.mood_list) - 1, self.mood_list.index(self.mood)

    def change_mood(self, type: str) -> None:
         min, max, current = self.get_mood_range()
         match type:
            case "+":
                if current < max:
                    self.mood = self.mood_list[current + 1]
            case "-":
                if current > min:
                    self.mood = self.mood_list[current - 1]
            case _:
                raise ValueError(f"{type} is not a valid mood option")

    def add_energy(self, min: int, max: int) -> None:
        # better mood adds more
        weighted_max = max + self.mood.value[1]
        if weighted_max <= min:
            weighted_max = min + 1
        self.energy += random.randint(min, weighted_max)

    def use_energy(self, min: int, max: int) -> None:
        # better mood uses less
        weighted_max = max - self.mood.value[1]
        if weighted_max <= min:
            weighted_max = min + 1
        self.energy += random.randint(min, weighted_max)

    def add_studio_time(self, min: int, max: int) -> None:
        # better mood adds less
        weighted_max = max - self.mood.value[1]
        if weighted_max <= min:
            weighted_max = min + 1
        self.studio_time += random.randint(min, weighted_max)

    def update_mood(self) -> None:
        if self.works:
            liked_overall = sum((work.liked.value[1] * work.value) for work in self.works)
            if liked_overall > 0:
                self.change_mood("+")
            elif liked_overall < 0:
                self.change_mood("-")

        if self.studio_time > (720 + self.energy):
            self.change_mood("-")

        if self.studio_time > (1440 + self.energy):
            self.change_mood("-")

    # move instance methods

    def move(self, new_location) -> None:
        self.prev_location = self.location
        self.location = new_location

    def back(self) -> None:
        self.prev_location, self.location = self.location, self.prev_location

    def quit(self) -> None:
        self.move(self.quit_loc)

    def setup(self) -> None:
        self.move(self.setup_loc)

    def lose(self, reason) -> None:
        self.status_reason = reason
        self.move(self.lose_loc)

    # action instance methods

    def drink_coffee(self) -> None:
        self.add_energy(5, 19)
        self.add_studio_time(1, 5)

    def nap(self) -> None:
        self.studio_time = 0
        self.change_mood("+")
        self.add_energy(10, 19)

    def create(self) -> None:
        mood_weight: int = self.mood.value[1]
        min, max, current = self.get_mood_range()
        mood_list = []
        if mood_weight > 0:
            mood_list = self.mood_list[1:]
        elif mood_weight < 0:
            mood_list = self.mood_list[:-1]
        else:
            mood_list - self.mood_list[1:-1]

        self.works.append(Artwork(random.choice(mood_list)))

    # setup instance methods

    def set_delay(self) -> None:
        self.delay += 2
        if self.delay > 7:
            self.delay = 1

    def set_width(self) -> int:
        self.terminal_width = shutil.get_terminal_size().columns
