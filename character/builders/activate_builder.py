from constants import characterParams, charNameTag
from utils import colorCodeHexGen

def activate_file_content(datapackParams):
    lines = [
        f"# Activates {characterParams.get('name')}",
        f"tag @s add {charNameTag}",
        f'tellraw @s [{{"text":"{characterParams.get("name")} activated!","color":"{colorCodeHexGen(characterParams.get("color_scheme")[0])}"}}]'
    ]
    return "\n".join(lines)