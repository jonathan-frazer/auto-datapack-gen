from constants import characterParams, charNameTag
from utils import colorCodeHexGen

def deactivate_file_content(datapackParams):
    lines = [
        f"# Deactivates {characterParams.get('name')}",
        f"tag @s remove {charNameTag}",
        f'tellraw @s [{{"text":"{characterParams.get("name")} deactivated!","color":"{colorCodeHexGen(characterParams.get("color_scheme")[1])}"}}]'
    ]
    return "\n".join(lines)