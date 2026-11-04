# untitled actions

import time
from enum import Enum

class GameAction(str, Enum):
    DRINK_COFFEE = 'drink_coffee'

def game_action(player: Player, action: str) -> None:
    match action:
        case GameAction.DRINK_COFFEE.lower():
            if player.energy_level < 30:
                player.energy_level += 20
                # could set this up to delay print or something
                print("\n* Gulp. Bitter, but it works! *")
                time.sleep(player.delay)
            else:
                print("\n* You're already buzzing on caffeine! *")
                time.sleep(player.delay)
