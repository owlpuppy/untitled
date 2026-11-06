# untitled actions

import time
from enum import Enum
from .entities import ArtType, Artwork, Player

class GameAction(str, Enum):
    DRINK_COFFEE = 'drink_coffee'
    SET_WIDTH = 'set_width'
    SET_DELAY = 'set_delay'

def game_action(player: Player, action: str) -> str | None:
    response = None

    match action:
        case GameAction.DRINK_COFFEE.value:
            player.drink_coffee()
            if player.energy < player.max_energy:
                response = "\n* Gulp. Bitter, but it works! *"
            elif player.energy < player.crit_energy:
                response = "\n* Your hands begin to shake, be careful! *"
            else:
                response = "\n* Not good, the room spins, panic sets in... *"
                player.lose("You drank too much coffee.")
        case GameAction.SET_WIDTH.value:
            player.set_width()
        case GameAction.SET_DELAY.value:
            player.set_delay()
        case None:
            pass
        case _:
            raise ValueError(f"{action} is not defined")

    return response
