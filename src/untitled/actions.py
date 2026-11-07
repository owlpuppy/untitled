# untitled actions

import random
from enum import Enum
from .entities import ArtType, Artwork, Player

class GameAction(str, Enum):
    DRINK_COFFEE = 'drink_coffee'
    SET_WIDTH = 'set_width'
    SET_DELAY = 'set_delay'

def game_action(player: Player, action: str | None, responses: dict | None) -> str | None:
    response = None

    match action:
        case GameAction.DRINK_COFFEE.value:
            if responses is None:
                raise ValueError(f"No responses found for {action}")

            player.drink_coffee()

            if player.energy < player.max_energy:
                response = random.choice(responses["1"])
            elif player.energy < player.crit_energy:
                response = random.choice(responses["2"])
            else:
                response, status = responses["lose"]
                player.lose(status)

        case GameAction.SET_WIDTH.value:
            player.set_width()

        case GameAction.SET_DELAY.value:
            player.set_delay()

        case None:
            pass

        case _:
            raise ValueError(f"{action} is not defined")

    return response
