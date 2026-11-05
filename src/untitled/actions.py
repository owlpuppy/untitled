# untitled actions

import time
from enum import Enum
from .entities import ArtType, Artwork, Player

class GameAction(str, Enum):
    DRINK_COFFEE = 'drink_coffee'

def game_action(player: Player, action: str) -> str | None:
    response = None

    match action:
        case GameAction.DRINK_COFFEE.value:
            player.drink_coffee()
            if player.energy_level < player.max_energy:
                response = "\n* Gulp. Bitter, but it works! *"
            elif player.energy_level < player.crit_energy:
                response = "\n* Your hands begin to shake, be careful! *"
            else:
                response = "\n* Not good, the room spins, panic sets in... *"
                player.lose("You drank too much coffee.")

    return response
