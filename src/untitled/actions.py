# untitled actions

import random
from enum import Enum
from .entities import ArtType, Artwork, Player

class GameAction(str, Enum):
    DRINK_COFFEE = 'drink_coffee'
    CREATE = 'create'
    NAP = "nap"
    SET_WIDTH = 'set_width'
    SET_DELAY = 'set_delay'

# helper functions

# main functions

def game_action(player: Player, action: str | None, responses: dict | None) -> str | None:
    if action == None:
        return None

    match action:
        case GameAction.DRINK_COFFEE.value:
            if responses is None:
                raise ValueError(f"No responses found for {action}")

            player.drink_coffee()

            if player.energy < player.max_energy:
                return random.choice(responses["1"])
            elif player.energy < player.crit_energy:
                return random.choice(responses["2"])
            else:
                response, status = responses["lose"]
                player.lose(status)
                return response

        case GameAction.CREATE.value:
            player.use_energy(5, 20)
            player.add_studio_time(30, 60)

            if player.energy < 0:
                response, status = responses["lose"]
                player.lose(status)
                return response

            if random.random() < player.mood.value[2]:
                response = random.choice(responses["2"])

            player.create()
            response = random.choice(responses["1"])
            response = response.replace("<< artwork title >>", player.works[-1].title)
            response = response.replace("<< player mood >>", player.mood.value[0])
            return response


        case GameAction.NAP.value:
            player.nap()
            # nap message

        case GameAction.SET_WIDTH.value:
            player.set_width()

        case GameAction.SET_DELAY.value:
            player.set_delay()

        case _:
            raise ValueError(f"{action} is not defined")
