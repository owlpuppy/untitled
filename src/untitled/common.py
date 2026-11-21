# untitled common

CANCEL_REQUEST = "-- request cancelled --"

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
    try:
        return int(raw)
    except ValueError:
        return False
    return False
