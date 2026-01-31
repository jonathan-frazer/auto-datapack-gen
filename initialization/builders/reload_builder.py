from constants import characterParams, charNameTag
from utils import colorCodeHexGen

def reload_file_content(datapackParams):
    def reload_string_gen():
        message = datapackParams.get('load_msg', 'Datapack Loaded!')
        colorScheme = characterParams.get('color_scheme', ['white'])

        words = message.split()
        formatted_words = []
        for i,word in enumerate(words):
            color = colorScheme[i % len(colorScheme)]
            formatted_words.append(f'{{"text":"{word} ","color":"{colorCodeHexGen(color)}"}}')

        return f'tellraw @a [{",".join(formatted_words)}]'

    lines = [
        "# Runs Once per World Load",
        reload_string_gen()
    ]

    lines.append(f"\nschedule function {datapackParams['namespace']}:main_sec 1t")
    lines.append(f"schedule function {datapackParams['namespace']}:main_halfsec 1t")

    return "\n".join(lines)