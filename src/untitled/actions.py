# untitled actions

import random, re
from enum import Enum
from .entities import ArtType, Artwork, Player, PlayerMood
from .common import get_player_input, get_player_input_as_int

class GameAction(str, Enum):
    DRINK_COFFEE = 'drink_coffee'
    CREATE = 'create'
    NAP = "nap"
    DELETE_WORK = 'delete_work'
    REWORK_WORK = 'rework_work'
    SELL_WORK = 'sell_work'
    SET_WIDTH = 'set_width'
    SET_DELAY = 'set_delay'

# helper functions

def get_response(responses: dict | None, response_type: str) -> str | tuple[str, str]:
    if responses is None:
        raise ValueError(f"No responses found for {action}")

    match response_type:
        case "success":
            return  random.choice(responses["1"]) if isinstance(responses["1"], list) else responses["1"]
        case "caution":
            return random.choice(responses["2"]) if isinstance(responses["2"], list) else responses["2"]
        case "fail":
            return random.choice(responses["fail"]) if isinstance(responses["fail"], list) else responses["fail"]
        case "lose":
            if len(responses["lose"]) != 2:
                raise ValueError(f"lose responses are not valid {action}")
            return tuple(responses["lose"])
        case _:
            raise ValueError(f"{response_type} is not a valid response type")

def take_input(msg: str) -> str | None:
    entered = re.sub(r'[^A-Za-z0-9 ]+', '', input(f"\n{msg} ").strip().lower())
    return entered

# main functions

def game_action(player: Player, action: str | None, responses: dict | None) -> str | None:
    if action == None:
        return None

    match action:
        case GameAction.DRINK_COFFEE.value:
            # drink coffee
            player.add_energy(5, 19)
            player.add_studio_time(1, 5)

            if player.energy < player.max_energy:
                return get_response(responses, "success")
            elif player.energy < player.crit_energy:
                return get_response(responses, "caution")
            else:
                response, status = get_response(responses, "lose")
                player.lose(status)
                return response

        case GameAction.CREATE.value:
            player.use_energy(5, 20)
            player.add_studio_time(30, 69)

            if player.energy < 0:
                response, status = responses["lose"]
                player.lose(status)
                return response

            if random.random() < player.mood.value[2]:
                return get_response(responses, "fail")

            player.create()
            response = get_response(responses, "success")
            response = response.replace("<< artwork title >>", player.works[-1].title)
            response = response.replace("<< player mood >>", player.mood.value[0])
            return response


        case GameAction.NAP.value:
            if not player.is_tired():
                return get_response(responses, "fail")
            # nap
            player.studio_time = 0
            player.change_mood("+")
            player.add_energy(10, 19)
            player.update_tired_weight(4, 69)

            if player.energy < player.max_energy:
                return get_response(responses, "success")
            elif player.energy < player.crit_energy:
                return get_response(responses, "caution")
            else:
                response, status = get_response(responses, "lose")
                player.lose(status)
                return response

        case GameAction.DELETE_WORK.value:
            if not player.works:
                return get_response(responses, "fail")

            entered = get_player_input_as_int("Which one?")
            ### its not an int
            if entered is not False:
                index = entered - 1
                if 0 <= index < len(player.works):
                    # random loss trap
                    if random.random() < 0.001:
                        response, status = get_response(responses, "lose")
                        player.lose(status)
                        return response
                    # removal action
                    del player.works[index]
                    # mistake trap
                    if player.is_very_tired() or player.is_grumpy():
                        if random.random() < 0.05:
                            mistake = random.randint(0, len(player.works) -1)
                            del player.works[mistake]
                            return get_response(responses, "caution")
                    return get_response(responses, "success")
                else:
                    return get_response(responses, "fail")
            else:
                return get_response(responses, "fail")

        case GameAction.REWORK_WORK.value:
            return 'xx action not implemented'

        case GameAction.SELL_WORK.value:
            return 'xx action not implemented'

        case GameAction.SET_WIDTH.value:
            player.set_width()

        case GameAction.SET_DELAY.value:
            player.set_delay()

        case _:
            raise ValueError(f"{action} is not defined")
