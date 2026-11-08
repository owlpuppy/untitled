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

class Player:
    # class variables
    max_energy: int = 50
    start_loc = "intro"
    quit_loc = "quit"
    lose_loc = "lose"
    setup_loc = "setup"

    # instance vars
    def __init__(self) -> None:
        self.works: list[Artwork] = []
        self.energy: int = random.randint(10, 35)
        self.mood: PlayerMood = PlayerMood.OKI
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

    def update_mood(self) -> None:
        if self.works:
            mood_list = list(PlayerMood)
            min, max, current = 0, len(mood_list) - 1, mood_list.index(self.mood)
            liked_overall = sum(work.liked.value[1] for work in self.works)
            if liked_overall > 0 and current < max:
                self.mood = mood_list[current + 1]
            elif liked_overall < 0 and current > min:
                self.mood = mood_list[current - 1]


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
        self.energy += random.randint(5, 19 + self.mood.value[1])

    # setup instance methods

    def set_delay(self) -> None:
        self.delay += 2
        if self.delay > 7:
            self.delay = 1

    def set_width(self) -> int:
        self.terminal_width = shutil.get_terminal_size().columns

class Artwork:
    def __init__(self, liked: PlayerMood) -> None:
        self.type: ArtType = random.choice(list(ArtType)).lower()
        self.value: int = random.randint(1, 20)
        self.liked: PlayerMood = liked

    @classmethod
    def create(cls, player: Player):
        mood_list = list(PlayerMood)
        mood_weight: int = player.mood.value[1]
        min, max, current = 0, len(mood_list) - 1, mood_list.index(player.mood)
        if mood_weight > 0:
            mood_list = mood_list[1:]
        elif mood_weight < 0:
            mood_list = mood_list[:-1]
        else:
            mood_list - mood_list[1:-1]
        return cls(random.choice(mood_list))

    def __eq__(self, other):
        if isinstance(other, Artwork):
            if (self.type == other.type and
                self.value is other.value and
                self.liked is other.liked):
                return True
        return False
