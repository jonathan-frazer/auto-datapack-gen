from constants import QPRESS_SCOREBOARD_NAME, RCLICK_SCOREBOARD_NAME, characterParams, charNameTag
from utils import colorCodeHexGen, nameShortener, get_action_slot_entries, ultimate_scoreboard_name


def reload_file_content(datapackParams):
    def format_load_message():
        message = datapackParams.get("load_msg", "Datapack Loaded!")
        color_scheme = characterParams.get("color_scheme", ["white"])
        words = message.split()
        formatted = []
        for i, word in enumerate(words):
            color = color_scheme[i % len(color_scheme)]
            formatted.append(f'{{"text":"{word} ","color":"{colorCodeHexGen(color)}"}}')
        return f"tellraw @a [{','.join(formatted)}]"

    def detect_click_drop(abilities):
        click = False
        drop = False
        for ability in abilities:
            if isinstance(ability, dict) and ability.get("ultimate"):
                return True, True
            if isinstance(ability, list):
                return True, True
            if isinstance(ability, dict):
                entries = get_action_slot_entries(ability.get("action_slots") or [])
                for entry in entries:
                    action = entry.get("action", "")
                    if not action:
                        continue
                    if action in ["r-click", "shift-click"]:
                        click = True
                    if action in ["q-press", "shift-q-press"]:
                        drop = True
                    if click and drop:
                        return True, True
        return click, drop

    def ability_scoreboards(ability, slot_index):
        lines = [f"#Slot {slot_index + 1}"]
        if isinstance(ability, list):
            lines.append(f"\t#Swap Cycle\n\tscoreboard objectives add {nameShortener(charNameTag, max_length=8)}{slot_index}Swap dummy")
            found = False
            for j, sub_ability in enumerate(ability):
                if isinstance(sub_ability, dict) and ("cooldown" in sub_ability or "sneakCooldown" in sub_ability):
                    if not found:
                        lines.append("\t#Cooldowns")
                        found = True
                    lines.append(f"\tscoreboard objectives add {nameShortener(sub_ability.get('name', f'SubAbility{j}'), max_length=12)}{slot_index}CD dummy")
            return lines

        if isinstance(ability, dict) and ability.get("ultimate"):
            lines.append("\t#Ultimate")
            lines.append(f"\tscoreboard objectives add {ultimate_scoreboard_name(ability.get('name', f'Ability{slot_index}'), slot_index)} dummy")
            lines.append("")
            return lines

        if isinstance(ability, dict):
            entries = get_action_slot_entries(ability.get("action_slots") or [])
            has_cd = any((e.get("cooldown") or 0) > 0 for e in entries)
            if has_cd:
                lines.append("\t#Cooldowns")
                lines.append(f"\tscoreboard objectives add {nameShortener(ability.get('name', f'Ability{slot_index}'), max_length=12)}{slot_index}CD dummy")

        lines.append("\t#User Defined Scoreboards")
        lines.append("")
        return lines

    abilities = characterParams.get("ability_slots", [])
    click, drop = detect_click_drop(abilities)

    scoreboard_lines = []
    for i, ability in enumerate(abilities):
        scoreboard_lines.extend(ability_scoreboards(ability, i))

    scoreboard_lines.append("")
    if click:
        scoreboard_lines.append(f"scoreboard objectives add {RCLICK_SCOREBOARD_NAME} used:warped_fungus_on_a_stick")
    if drop:
        scoreboard_lines.append(f"scoreboard objectives add {QPRESS_SCOREBOARD_NAME} dropped:warped_fungus_on_a_stick")
    scoreboard_lines.append("scoreboard objectives add SelectedSlot dummy")

    lines = [
        "# Runs Once per World Load",
        format_load_message(),
        "",
        "# Scoreboards",
        "\n".join(scoreboard_lines),
        "",
        "#Schedule Functions",
        f"schedule function {datapackParams['namespace']}:main_sec 1t",
        f"schedule function {datapackParams['namespace']}:main_halfsec 1t",
    ]

    return "\n".join(lines)
