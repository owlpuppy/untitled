# untitled engine

import sys, os, errno, tomllib, shutil, time
from pathlib import Path
#from .entities import ArtType, Artwork, Player

# helper functions

def load_toml(file: str = '') -> dict:
    if file == '':
        raise ValueError("no file given to load")

    toml_path = Path(__file__).parent / f"{file}.toml"

    if not toml_path.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), toml_path)

    with open(toml_path, "rb") as f:
        return tomllib.load(f)

def game_status(energy_level: int = 0, node: dict | None = None) -> str: # will need to pass player: Player in when that's done and remove energy
    if node is None:
        return "Hi there!"
    else:
        if 'status' in node:
            if 'type' in node['status']:
                match node['status']['type']:
                    case 'text':
                        return node['status']['text']
                    case 'game_stats':
                        return f'[Energy: {energy_level}]' # will need to change to player.energy_level
                    case _:
                        raise ValueError(f"status type in {node} is not valid")
            else:
                raise ValueError(f"no status in {node}")
        else:
            return ' '


def display_story(energy_level: int, terminal_width: int, node: dict) -> bool:
    head_separator = "="
    div_separator = "-"
    story_to_screen = f"""{head_separator * terminal_width}
untitled
{head_separator * terminal_width}
{game_status(energy_level, node)}
{div_separator * terminal_width}
{node['text']}
{div_separator * terminal_width}
"""

    if "choices" not in node or not node["choices"]:
        story_to_screen += "\n*** THE END ***\n"
        print("\033[H\033[J", end="")
        print(story_to_screen)
        return False

    for choice, description in node["choices"].items():
        story_to_screen += f"\n[{choice}] {description['text']}"

    print("\033[H\033[J", end="")
    print(story_to_screen)
    return True


# primary function

def start_game() -> None:
    story = load_toml("story")
    #player = Player("intro", "quit", shutil.get_terminal_size().columns)
    start_node = "intro"
    quit_node = "quit"
    current_node = start_node

    energy_level = 10
    delay = 5

    #os.system('cls' if os.name == 'nt' else 'clear')
    terminal_width = shutil.get_terminal_size().columns

    while True:
        node = story[current_node]
        keep_playing = display_story(energy_level, terminal_width, node)

        if keep_playing == False:
            break

        entered = input("\nChoose an option: ").strip()

        if entered in node["choices"]:
            chosen = node["choices"][entered]
            # .get() prevents crashing if 'action' is missing in TOML
            action = chosen.get("action")

            if action == "drink_coffee":
                if energy_level < 30:
                    energy_level += 20
                    # could set this up to delay print or something
                    print("\n* Gulp. Bitter, but it works! *")
                    time.sleep(delay)
                else:
                    print("\n* You're already buzzing on caffeine! *")
                    time.sleep(delay)

            current_node = chosen["target"]

        elif entered.lower() == "quit":
            current_node = end_node

        else:
            print("\n>> try again <<")
            time.sleep(delay)
