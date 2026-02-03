from constants import QPRESS_SCOREBOARD_NAME, RCLICK_SCOREBOARD_NAME, charNamespace, characterParams, charNameTag
from utils import nameShortener, get_action_slot_entries


def tick_file_content(datapackParams):
    def generate_interact_detectors():
        all_ability_lines = []
        abilities = characterParams.get(
            "ability_slots",
            [
                {"name": "Ability 1", "action_slots": ["r-click"]},
                {"name": "Ability 2", "action_slots": ["r-click"]},
                {"name": "Ability 3", "action_slots": ["r-click"]},
                {"name": "Ability 4", "action_slots": ["r-click"]},
            ],
        )

        for i, ability in enumerate(abilities):
            if isinstance(ability, list):
                ability_lines = [
                    f"\t#Slot {i+1}",
                    f"\texecute if score @s[scores={{SelectedSlot={i}}}] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/qpress/0_check",
                ]

                for j, sub_ability in enumerate(ability):
                    ability_lines.append(f"\t\t#{sub_ability.get('name', f'SubAbility {j+1}')}")
                    if isinstance(sub_ability, dict) and sub_ability.get("sneakCooldown", 0):
                        ability_lines.append(
                            f"\t\texecute if score @s[predicate=!{datapackParams['namespace']}:is_sneaking,scores={{SelectedSlot={i},{nameShortener(charNameTag, max_length=8)}{i}Swap={j}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(sub_ability.get('name', 'SubAbility'), max_length=16, type='namespace')}/rclick/0_check"
                        )
                        ability_lines.append(
                            f"\t\texecute if score @s[predicate={datapackParams['namespace']}:is_sneaking,scores={{SelectedSlot={i},{nameShortener(charNameTag, max_length=8)}{i}Swap={j}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(sub_ability.get('name', 'SubAbility'), max_length=16, type='namespace')}/shiftclick/0_check"
                        )
                    else:
                        ability_lines.append(
                            f"\t\texecute if score @s[scores={{SelectedSlot={i},{nameShortener(charNameTag, max_length=8)}{i}Swap={j}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(sub_ability.get('name', 'SubAbility'), max_length=16, type='namespace')}/rclick/0_check"
                        )
                    ability_lines.append("")
                ability_lines.append("")
                all_ability_lines.append("\n".join(ability_lines))
                continue

            ability_lines = [f"\t#Slot {i+1}"]
            if isinstance(ability, dict):
                if ability.get("ultimate"):
                    slot_names = ["r-click", "q-press"]
                else:
                    entries = get_action_slot_entries(ability.get("action_slots", ["f-press", "q-press", "r-click"]))
                    slot_names = [e["action"] for e in entries]
                    if "f-press" not in slot_names:
                        slot_names.append("f-press")
                    if "q-press" not in slot_names:
                        slot_names.append("q-press")

                if "r-click" in slot_names:
                    if "shift-click" not in slot_names:
                        ability_lines.append(
                            f"\texecute if score @s[scores={{SelectedSlot={i}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/rclick/0_check"
                        )
                    else:
                        ability_lines.append(
                            f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate=!{datapackParams.get('namespace')}:is_sneaking] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/rclick/0_check"
                        )
                        ability_lines.append(
                            f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shiftclick/0_check"
                        )
                elif "shift-click" in slot_names:
                    ability_lines.append(
                        f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shiftclick/0_check"
                    )

                if "q-press" in slot_names:
                    if "shift-q-press" not in slot_names:
                        ability_lines.append(
                            f"\texecute if score @s[scores={{SelectedSlot={i}}}] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/qpress/0_check"
                        )
                    else:
                        ability_lines.append(
                            f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate=!{datapackParams.get('namespace')}:is_sneaking] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/qpress/0_check"
                        )
                        ability_lines.append(
                            f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shift_qpress/0_check"
                        )
                elif "shift-q-press" in slot_names:
                    ability_lines.append(
                        f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shift_qpress/0_check"
                    )

            all_ability_lines.append("\n".join(ability_lines))

        yield "\n\n".join(all_ability_lines)

    lines = [
        "# Runs Every Tick",
        "execute store result score @s SelectedSlot run data get entity @s SelectedItemSlot",
        "# Ability",
        "\n\n".join(line for line in generate_interact_detectors()),
    ]

    abilities = characterParams.get("ability_slots", [])
    click = False
    drop = False
    for ability in abilities:
        if isinstance(ability, list):
            click = True
            drop = True
            break
        if isinstance(ability, dict):
            if ability.get("ultimate"):
                click = True
                drop = True
                break
            entries = get_action_slot_entries(ability.get("action_slots", []))
            for entry in entries:
                slot = entry["action"]
                if slot in ["r-click", "shift-click"]:
                    click = True
                if slot in ["q-press", "shift-q-press"]:
                    drop = True
                if click and drop:
                    break
        if click and drop:
            break

    if click:
        lines.append(f"scoreboard players reset @s {RCLICK_SCOREBOARD_NAME}")
    if drop:
        lines.append(f"scoreboard players reset @s {QPRESS_SCOREBOARD_NAME}")

    return "\n".join(lines)
