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
    GRRR = "grrr", -6, 0.5
    BLEGH = "blegh", -3, 0.40
    OKI = "oki", 1, 0.25
    COLON_THREE = ":3", 3, 0.15
    UWU = "uwu", 5, 0.05

    def __init__(self, value, weight, chance):
        self._value_ = value
        self.weight = weight
        self.chance = chance

class Artwork:
    #class variables
    min_value = 1
    max_value = 20

    def __init__(self, liked: PlayerMood, title: str, kind: ArtType, value: int) -> None:
        self.kind: ArtType = kind
        self.value: int = value
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

        return cls(liked, " ".join(words).title(), random.choice(list(ArtType)).value, random.randint(cls.min_value, cls.max_value))

    def __eq__(self, other):
        if isinstance(other, Artwork):
            if (self.kind == other.kind and
                self.value == other.value and
                self.liked is other.liked and
                self.title == other.title):
                return True
        return False

    def __repr__(self):
        return f"# Title: {self.title}, Type: {self.kind}, Value: {self.value}, Liked: {self.liked.value} #"

    def __str__(self):
        return f"Title: {self.title}, Type: {self.kind}, Value: {self.value}, Liked: {self.liked.value}"

class Player:
    # class variables
    max_energy: int = 50
    start_loc = "intro"
    quit_loc = "quit"
    lose_loc = "lose"
    setup_loc = "setup"
    mood_list = list(PlayerMood)

    # instance vars
    def __init__(self, energy: int, tired_weight: int, crit_energy: int, win_value: int, terminal_width: int) -> None:
        self.works: list[Artwork] = []
        self.energy: int = energy
        self.tired_weight = tired_weight
        self.mood: PlayerMood = PlayerMood.OKI
        self.time_awake = 0
        self.crit_energy: int = crit_energy
        self.win_value: int = win_value
        self.location: str = self.start_loc
        self.prev_location: str | None = None
        self.delay: int = 5
        self.terminal_width: int = terminal_width
        self.status_reason = None

    @classmethod
    def start_playing(cls):
        energy = random.randint(10, 35)
        tired_weight = random.randint(-69, 69)
        crit_energy = random.randint(60, 75)
        win_value = random.randint(100, 500)
        terminal_width = shutil.get_terminal_size().columns
        return cls(energy, tired_weight, crit_energy, win_value, terminal_width)

    #magic methods

    def __repr__(self):
        response = (f"# Energy(current/max/crit):{self.energy}/{self.max_energy}/{self.crit_energy}, "
                    "Locations(start,quit,lose,setup,current,previous):"
                    f"{self.start_loc}/{self.quit_loc}/{self.lose_loc}/{self.setup_loc}/{self.location}/{self.prev_location}, "
                    f"Moods:{[mood.value[0] for mood in self.mood_list]}, Works:{self.works}, TimeAwake:{self.time_awake}, "
                    f"Mood:{self.mood.value}, WinValue:{self.win_value}, TiredWeight:{self.tired_weight}, "
                    f"Setup(TermWidth/Delay): {self.terminal_width}/{self.delay} #")
        return response

    def __str__(self):
        response = (f"Energy(current/max/crit):{self.energy}/{self.max_energy}/{self.crit_energy}, "
                    "Locations(start,quit,lose,setup,current,previous):"
                    f"{self.start_loc}/{self.quit_loc}/{self.lose_loc}/{self.setup_loc}/{self.location}/{self.prev_location}, "
                    f"Moods:{[mood.value[0] for mood in self.mood_list]}, Works:{self.works}, TimeAwake:{self.time_awake}, "
                    f"Mood:{self.mood.value}, WinValue:{self.win_value}, TiredWeight:{self.tired_weight}, "
                    f"Setup(TermWidth/Delay): {self.terminal_width}/{self.delay}")
        return response

    # mechanic instance methods

    def won_by_value(self) -> bool:
        if self.works:
            total_value = sum(work.value for work in self.works)
            if total_value >= self.win_value:
                return True
        return False

    def get_mood_range(self) -> tuple[int, int, int]:
        return 0, len(self.mood_list) - 1, self.mood_list.index(self.mood)

    def change_mood(self, mood_type: str) -> None:
         low, high, current = self.get_mood_range()
         match mood_type:
            case "+":
                if current < high:
                    self.mood = self.mood_list[current + 1]
            case "-":
                if current > low:
                    self.mood = self.mood_list[current - 1]
            case _:
                raise ValueError(f"{mood_type} is not a valid mood option")

    def add_energy(self, low: int, high: int) -> None:
        # better mood adds more
        weighted_high = high + self.mood.weight
        if weighted_high <= low:
            weighted_high = low + 2
        self.energy += random.randint(low, weighted_high)

    def use_energy(self, low: int, high: int) -> None:
        # better mood uses less
        weighted_high = high - self.mood.weight
        if weighted_high <= low:
            weighted_high = low + 1
        self.energy -= random.randint(low, weighted_high)

    def add_time_awake(self, low: int, high: int) -> None:
        # better mood adds less
        weighted_high = high - self.mood.weight
        if weighted_high <= low:
            weighted_high = low + 2
        self.time_awake += random.randint(low, weighted_high)

    def is_tired(self) -> bool:
        if self.time_awake > (480 + self.tired_weight):
            return True
        return False

    def is_very_tired(self) -> bool:
        if self.time_awake > (960 + self.tired_weight):
            return True
        return False

    def is_grumpy(self) -> bool:
        if self.mood is PlayerMood.GRRR:
            return True
        return False

    def is_overworked(self) -> bool:
        if self.time_awake > (1440 + self.tired_weight):
            return True
        return False

    def update_mood(self) -> None:
        if self.works:
            liked_overall = sum((work.liked.weight * work.value) for work in self.works) / sum((work.value) for work in self.works)
            self.mood = min(PlayerMood, key=lambda mood: abs(mood.weight - liked_overall))
        else:
            self.mood = PlayerMood.OKI

        if self.is_tired():
            self.change_mood("-")

        if self.is_very_tired():
            self.change_mood("-")

    def update_tired_weight(self, low: int, high: int) -> None:
        if self.mood.weight < 1:
            self.tired_weight -= random.randint(low, high)
        else:
            self.tired_weight += random.randint(low, high)

        if self.tired_weight > self.energy:
            self.tired_weight = self.energy

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

    def create(self) -> None:
        min, max, current = self.get_mood_range()
        mood_list = []
        match self.mood:
            case PlayerMood.GRRR:
                mood_list = self.mood_list[:-2]
            case PlayerMood.BLEGH:
                mood_list = self.mood_list[:-1]
            case PlayerMood.OKI:
                mood_list = self.mood_list[1:-1]
            case _:
                mood_list = self.mood_list[1:]

        self.works.append(Artwork.create(random.choice(mood_list)))

    # setup instance methods

    def set_delay(self) -> None:
        if self.delay > 7:
            self.delay = 1
        else:
            self.delay += 2

    def set_width(self) -> int:
        self.terminal_width = shutil.get_terminal_size().columns
