# untitled render

from .entities import ArtType, Artwork, Player

def game_status(player: Player, node: dict) -> str:
    status_response = ''

    if 'status' in node:
        status_text, status_type = node['status'].get("text"), node['status'].get('type')

        if status_type is not None:
            match status_type:
                case 'game_stats':
                    status_response += f'[Energy: {player.energy}/{player.max_energy}] [{player.location}]'
                case 'setup_stats':
                    status_response += f'[delay: {player.delay} sec] [terminal width: {player.terminal_width}] '
                case _:
                    raise ValueError(f"status type in {player.location} is not valid")

        if status_text is not None:
            status_response += status_text

        if player.status_reason is not None:
            status_response += player.status_reason

    return status_response

def game_commands(node: dict) -> str:
    command_type = 'show'
    command_response = 'type to quit, setup'
    if 'commands' in node:
        command_type = node['commands'].get('type')
        match command_type:
            case 'hide':
                command_response = ''
            case _:
                raise ValueError(f'{command_type} not recognized')

    return command_response

def refresh_story(player: Player, node: dict) -> tuple[str, bool]:
    head_separator = "="
    div_separator = "-"
    story_to_screen = f"""{head_separator * player.terminal_width}
untitled
{head_separator * player.terminal_width}
{game_status(player, node)}
{div_separator * player.terminal_width}

{node['text']}

{div_separator * player.terminal_width}
{game_commands(node)}
"""

    if not node.get("choices"):
        story_to_screen += "\n*** THE END ***\n"
        return (story_to_screen, False)

    for choice, description in node["choices"].items():
        story_to_screen += f"\n[{choice}] {description['text']}"

    return (story_to_screen, True)
