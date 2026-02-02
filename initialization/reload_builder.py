from constants import QPRESS_SCOREBOARD_NAME, RCLICK_SCOREBOARD_NAME, characterParams, charNameTag
from utils import colorCodeHexGen, nameShortener
from collections import deque

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

    def load_scores():
        abilities = characterParams.get('ability_slots',[])
        click = False
        drop = False

        for ability in abilities:
            if isinstance(ability,dict):
                slots = ability.get('action_slots')
                for slot in slots:
                    if slot in ["r-click","shift-click"]:
                        click = True
                    if slot in ['q-press','shift-q-press']:
                        drop = True
                    if click and drop:
                        break

            if click and drop:
                break
        
        lines = []
        found = False
        for i,ability in enumerate(abilities):
            if isinstance(ability,list):
                click = True
                drop = True
                if not found:
                    lines.append("#MultiTool Swapping Scores")
                    found = True
                lines.append(f"scoreboard objectives add {nameShortener(charNameTag,max_length=8,type='namespace')}{i}Swap dummy")
        
        basicLines = [
            f"scoreboard objectives add {RCLICK_SCOREBOARD_NAME} used:warped_fungus_on_a_stick" if click else "",
            f"scoreboard objectives add {QPRESS_SCOREBOARD_NAME} dropped:warped_fungus_on_a_stick" if drop else "",
            f"scoreboard objectives add SelectedSlot dummy"
        ]
        lines.append("")
        lines.extend(basicLines)

        return "\n".join(lines)


    lines = [
        "# Runs Once per World Load",
        reload_string_gen(),
        "\n# Scores",
        load_scores()
    ]

    lines.append(f"\n#Schedule Functions")
    lines.append(f"schedule function {datapackParams['namespace']}:main_sec 1t")
    lines.append(f"schedule function {datapackParams['namespace']}:main_halfsec 1t")

    return "\n".join(lines)