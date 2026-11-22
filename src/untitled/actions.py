# untitled actions

import random, re
from enum import Enum
from .entities import ArtType, Artwork, Player, PlayerMood
from .common import get_player_input, get_player_input_as_int, CANCEL_REQUEST

class GameAction(str, Enum):
    DRINK_COFFEE = 'drink_coffee'
    CREATE = 'create'
    NAP = "nap",
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
        case "error":
            return f'>> {random.choice(responses["error"])} <<' if isinstance(responses["error"], list) else f'>> {responses["error"]} <<'
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
            # random fail
            if random.random() < 0.005:
                return get_response(responses, "fail")
            # drink coffee
            player.add_energy(5, 19)
            player.add_time_awake(1, 5)

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
            player.add_time_awake(30, 69)

            if player.energy < 0:
                response, status = responses["lose"]
                player.lose(status)
                return response

            if random.random() < player.mood.chance:
                return get_response(responses, "fail")

            player.create()
            # used all your energy
            if random.random() < 0.005:
                player.energy = 0;
                response = get_response(responses, "caution")
                return response.replace("<< artwork title >>", player.works[-1].title)
            # regular response
            response = get_response(responses, "success")
            response = response.replace("<< artwork title >>", player.works[-1].title)
            response = response.replace("<< player mood >>", player.mood.value)
            return response

        case GameAction.NAP.value:
            # not tired, no sleep
            if not player.is_tired():
                return get_response(responses, "error")
            # 5% failure chance to sleep
            if random.random() < 0.05:
                player.add_time_awake(3, 9)
                return get_response(responses, "fail")
            # nap
            player.time_awake = 0
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
                return get_response(responses, "error")

            entered = get_player_input_as_int("Which one?")

            if entered is None:
                return CANCEL_REQUEST
            if entered is False:
                return get_response(responses, "error")

            index = entered - 1
            if 0 <= index < len(player.works):
                # random loss
                if random.random() < 0.001:
                    response, status = get_response(responses, "lose")
                    player.lose(status)
                    return response
                # random fail
                if random.random() < 0.01:
                    player.add_time_awake(2, 5)
                    return get_response(responses, "fail")
                # removal action
                player.add_time_awake(3, 7)
                del player.works[index]
                # mistake trap
                if player.is_very_tired() or player.is_grumpy():
                    works_remaining = len(player.works)
                    if random.random() < 0.05 and works_remaining > 0:
                        mistake = random.randint(0, works_remaining -1) if works_remaining > 1 else 0
                        del player.works[mistake]
                        return get_response(responses, "caution")
                return get_response(responses, "success")
            return get_response(responses, "error")

        case GameAction.REWORK_WORK.value:
            if not player.works:
                return get_response(responses, "error")

            entered = get_player_input_as_int("Which one?")

            if entered is None:
                return CANCEL_REQUEST
            if entered is False:
                return get_response(responses, "error")

            index = entered - 1

            if not (0 <= index < len(player.works)):
                return get_response(responses, "error")

            player.use_energy(5, 10)
            player.add_time_awake(15, 42)
            # too much energy used
            if player.energy < 0:
                response, status = responses["lose"]
                player.lose(status)
                return response
            # random failure
            if random.random() < 0.05:
               return  get_response(responses, "fail")
            # going to rework based on mood
            to_edit = player.works[index]
            liked_index = player.mood_list.index(to_edit.liked)

            if random.random() < player.mood.chance:
                # bad result
                to_edit.liked = player.mood_list[liked_index - 1] if liked_index > 0 else player.mood_list[0]
                if not to_edit.is_liked():
                    # not liked, make it worth more
                    new_min = to_edit.value + 1
                    new_max = to_edit.max_value - player.mood.weight
                else:
                    # liked, make it worth less
                    new_min = to_edit.min_value
                    new_max = to_edit.value - 1
                to_edit.value = random.randint(new_min, new_max) if new_min < new_max else new_min
                return get_response(responses, "caution")

            # good result
            to_edit.liked = player.mood_list[liked_index + 1] if liked_index < len(player.mood_list) else player.mood_list[-1]
            if to_edit.is_liked():
                # liked, make it worth more
                new_min = to_edit.value + 1
                new_max = to_edit.max_value + player.mood.weight
            else:
                # not liked, make it worth less
                new_min = to_edit.min_value
                new_max = to_edit.value - 1
            to_edit.value = random.randint(new_min, new_max) if new_min < new_max else new_min
            return get_response(responses, "success")

        case GameAction.SELL_WORK.value:
            return 'xx action not implemented'

        case GameAction.SET_WIDTH.value:
            player.set_width()

        case GameAction.SET_DELAY.value:
            player.set_delay()

        case _:
            raise ValueError(f"{action} is not defined")
