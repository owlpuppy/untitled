# untitled render

from .entities import ArtType, Artwork, Player

# helper functions

def game_status(player: Player, node: dict) -> str:
    status_response = ''

    if 'status' in node:
        status_text, status_type = node['status'].get("text"), node['status'].get('type')

        if status_type is not None:
            match status_type:
                case 'game_stats':
                    energy = f'[Energy: {player.energy}/{player.max_energy}]'
                    mood = f'[Mood: {player.mood.value[0]}]'
                    studio_hours, studio_minutes = divmod(player.studio_time, 60) if player.studio_time > 0 else (0, 0)
                    studio_time = f'[Studio time: {studio_hours}h:{studio_minutes}m]'
                    tired = 'very tired!!' if player.is_very_tired() else 'tired!!' if player.is_tired() else ''
                    status_response += f'{energy} {studio_time} {mood}   [{player.location}] {tired}'
                case 'setup_stats':
                    status_response += f'[delay: {player.delay} sec] [terminal width: {player.terminal_width}] '
                case _:
                    raise ValueError(f"status type in {player.location} is not valid")

        if status_text is not None:
            status_response += status_text

        if player.status_reason is not None:
            status_response += player.status_reason

    return status_response

def story_content(player: Player, node: dict) -> str:
    story_text = node['text']
    if 'story' in node:
        story_type =  node['story'].get('type')

        if story_type is not None and isinstance(story_text, list):
            match story_type:
                case 'studio_time':
                    index = 0
                    if player.is_tired():
                        index += 1
                    if player.is_very_tired():
                        index += 1
                    if index in range(len(story_text)):
                        return story_text[index]
                    return story_text[-1] if index != 0 else story_text[0]
                case 'random':
                    return random.choice(story_text)
                case _:
                    raise ValueError(f'{story_type} not recognized')
    return story_text

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

# main functions

def refresh_story(player: Player, node: dict) -> tuple[str, bool]:
    head_separator = "="
    div_separator = "-"
    story_to_screen = f"""{head_separator * player.terminal_width}
untitled
{head_separator * player.terminal_width}
{game_status(player, node)}
{div_separator * player.terminal_width}

{story_content(player, node)}

{div_separator * player.terminal_width}
{game_commands(node)}
"""

    if not node.get("choices"):
        story_to_screen += "\n*** THE END ***\n"
        return (story_to_screen, False)

    for choice, description in node["choices"].items():
        story_to_screen += f"\n[{choice}] {description['text']}"

    return (story_to_screen, True)
