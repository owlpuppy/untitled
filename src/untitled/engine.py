# untitled engine

import sys, os, errno, tomllib, shutil, time
from pathlib import Path
from .entities import ArtType, Artwork, Player
from .actions import game_action
from .render import game_status, refresh_story

# helper functions

def load_toml(file: str = '') -> dict:
    if file == '':
        raise ValueError("no file given to load")

    toml_path = Path(__file__).parent / f"{file}.toml"

    if not toml_path.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), toml_path)

    with open(toml_path, "rb") as f:
        return tomllib.load(f)


# primary function

def start_game() -> None:
    story = load_toml("story")
    player = Player(shutil.get_terminal_size().columns)

    while True:
        node = story[player.location]
        display_story, keep_playing = refresh_story(player, node)

        print("\033[H\033[J", end="")
        print(display_story)
        if keep_playing == False:
            break

        entered = input("\nChoose an option: ").strip().lower()

        reply = None

        if entered in node["choices"]:
            chosen = node["choices"][entered]
            target = chosen.get("target")
            # .get() prevents crashing if 'action' is missing in TOML
            reply = game_action(player, chosen.get("action"))
            if target is not None:
                player.move(target)

        elif entered == "quit":
            player.quit()

        else:
            reply = "\n>> try again <<"

        if reply is not None:
            print(reply)
            time.sleep(player.delay)
