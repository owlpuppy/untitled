# untitled common
import os, logging

ABSPATH = os.path.abspath("./")

CANCEL_REQUEST = "-- request cancelled --"

logger = logging.getLogger("untitled")

def value_to_int(value) -> int | bool:
    if value is None or value is False:
        return value
    try:
        return int(value)
    except ValueError:
        return False

def get_player_input(msg: str) -> str | bool:
    entered = input(f"\n{msg} ").strip().lower()
    if entered is False or len(entered) < 1:
        return False
    if entered == "x":
        return None
    return entered

def get_player_input_as_int(msg: str) -> int | bool:
    raw = get_player_input(msg)
    if raw is None or raw is False:
        return raw
    return value_to_int(raw)
