# untitled entities

import shutil, random
from enum import Enum

class ArtType(Enum):
    PAINTING = 'painting'
    DRAWING = 'drawing'
    # can add more

class ArtTitle(Enum):
    PREFIX = ('beautiful', 'sticky', 'ephemeral', 'moody', 'experimental', 'untitled', 'aged', 'worn', 'bright')
    BASE = ('banana', 'cookie', 'tuna', 'brick', 'box', 'hat', 'shoe', 'marmalade', 'textbook', 'strainer', 'wall', 'tree')
    LINKAGE = ('in', 'of', 'from', 'as', 'with')
    EMOTION = ('sadness', 'anger', 'joy', 'jealousy', 'bliss', 'peace')

class PlayerMood(Enum):
    GRRR = "grrr", -5, 0.5
    BLEGH = "blegh", -2, 0.40
    OKI = "oki", 0, 0.25
    COLON_THREE = ":3", 2, 0.15
    UWU = "uwu", 5, 0.05

class Artwork:
    def __init__(self, liked: PlayerMood, title: str) -> None:
        self.type: ArtType = random.choice(list(ArtType)).value
        self.value: int = random.randint(1, 20)
        self.liked: PlayerMood = liked
        self.title: str = title

    @classmethod
    def create(cls, liked: PlayerMood):
        words = []

        if random.random() < 0.73:
            words.append(random.choice(ArtTitle.PREFIX.value))

        words.append(random.choice(ArtTitle.BASE.value))

        if random.random() < 0.39:
            words.append(random.choice(ArtTitle.LINKAGE.value))
            words.append(random.choice(ArtTitle.EMOTION.value))

        if random.random() < 0.23:
            words.append(f'number {random.randint(1,19)}')

        return cls(liked, " ".join(words).title())

    def __eq__(self, other):
        if isinstance(other, Artwork):
            if (self.type == other.type and
                self.value is other.value and
                self.liked is other.liked and
                self.title == other.title):
                return True
        return False

    def __repr__(self):
        return f"# Title: {self.title}, Type: {self.type}, Value: {self.value}, Liked: {self.liked.value[0]} #"

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
        self.energy -= random.randint(min, weighted_max)

    def add_studio_time(self, min: int, max: int) -> None:
        # better mood adds less
        weighted_max = max - self.mood.value[1]
        if weighted_max <= min:
            weighted_max = min + 1
        self.studio_time += random.randint(min, weighted_max)

    def is_tired(self) -> bool:
        if self.studio_time > (480 + self.energy):
            return True
        return False

    def is_very_tired(self) -> bool:
        if self.studio_time > (960 + self.energy):
            return True
        return False

    def is_overworked(self) -> bool:
        if self.studio_time > (1440 + self.energy):
            return True
        return False

    def update_mood(self) -> None:
        if self.works:
            liked_overall = sum((work.liked.value[1] * work.value) for work in self.works) / sum((work.value) for work in self.works)
            self.mood = min(PlayerMood, key=lambda mood: abs(mood.value[1] - liked_overall))

        if self.is_tired():
            self.change_mood("-")

        if self.is_very_tired():
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
            mood_list = self.mood_list[1:-1]

        self.works.append(Artwork.create(random.choice(mood_list)))

    # setup instance methods

    def set_delay(self) -> None:
        self.delay += 2
        if self.delay > 7:
            self.delay = 1

    def set_width(self) -> int:
        self.terminal_width = shutil.get_terminal_size().columns
