from constants import charNamespace, characterParams, charNameTag, ITEM_CUSTOM_DATA_COMPONENT
from utils import colorCodeHexGen, nameShortener, get_action_slot_entries, ultimate_scoreboard_name


def activate_file_content(datapackParams):
    def initialize_scoreboards():
        lines = ["#Initialize Scoreboards"]
        abilities = characterParams.get("ability_slots", [])

        for i, ability in enumerate(abilities):
            lines.append(f"#Slot {i+1}")
            if isinstance(ability, list):
                lines.append(f"\t#Swap Cycle\n\tscoreboard players set @s {nameShortener(charNameTag, max_length=8)}{i}Swap 0")
                found = False
                for j, sub_ability in enumerate(ability):
                    if isinstance(sub_ability, dict) and ("cooldown" in sub_ability or "sneakCooldown" in sub_ability):
                        if not found:
                            lines.append("\t#Cooldowns")
                            found = True
                        lines.append(
                            f"\texecute unless score @s {nameShortener(sub_ability.get('name', f'SubAbility{j}'), max_length=12)}{i}CD matches 1.. run scoreboard players set @s {nameShortener(sub_ability.get('name', f'SubAbility{j}'), max_length=12)}{i}CD 0"
                        )
                continue

            if isinstance(ability, dict):
                if ability.get("ultimate"):
                    ult = ultimate_scoreboard_name(ability.get("name", f"Ability{i}"), i)
                    lines.append("\t#Ultimate")
                    lines.append(f"\texecute unless score @s {ult} matches 1.. run scoreboard players set @s {ult} 0")
                    lines.append("")
                    continue

                entries = get_action_slot_entries(ability.get("action_slots", []))
                has_cd = any(e.get("cooldown", 0) > 0 for e in entries)
                if has_cd:
                    lines.append("\t#Cooldowns")
                    lines.append(
                        f"\texecute unless score @s {nameShortener(ability.get('name', f'Ability{i}'), max_length=12)}{i}CD matches 1.. run scoreboard players set @s {nameShortener(ability.get('name', f'Ability{i}'), max_length=12)}{i}CD 0"
                    )
            lines.append("\t#User Defined Scoreboards")
            lines.append("")

        return "\n".join(lines)

    lines = [
        f"# Activates {characterParams.get('name')}",
        f'tellraw @s [{{"text":"{characterParams.get("name")} activated!","color":"{colorCodeHexGen(characterParams.get("color_scheme")[0])}"}}]',
        f"tag @s add {charNameTag}",
        "",
        "#Apply Effects",
        f"function {datapackParams['namespace']}:{charNamespace}/effect",
        "",
        initialize_scoreboards(),
    ]
    return "\n".join(lines)


def deactivate_file_content(datapackParams):
    def delete_ability_item():
        if not isinstance(characterParams, dict):
            return ""
        ability_slots = characterParams.get("ability_slots", [])
        return f"#Delete Ability Items\nclear @s minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT}]{f' {len(ability_slots)}' if ability_slots else ''}"

    def delete_armor_line():
        armor_pieces = ["chestplate", "leggings", "boots"]
        armor = characterParams.get("armor", [])
        padded_armor = list(armor)[:3] + ["leather"] * (3 - len(armor))
        for i in range(3):
            armor_piece = armor_pieces[i]
            material = padded_armor[i]
            yield f"clear @s {material}_{armor_piece}[custom_data={ITEM_CUSTOM_DATA_COMPONENT}]"

    def delete_effects():
        effects = characterParams.get("effects", [])
        for effect in effects:
            effect_name = effect if isinstance(effect, str) else effect.get("name")
            yield f"effect clear @s minecraft:{effect_name}"

    def reset_scoreboards():
        lines = ["#Reset Scoreboards"]
        abilities = characterParams.get("ability_slots", [])

        for i, ability in enumerate(abilities):
            lines.append(f"#Slot {i+1}")
            if isinstance(ability, list):
                lines.append(f"\t#Swap Cycle\n\tscoreboard players reset @s {nameShortener(charNameTag, max_length=8)}{i}Swap")
                found = False
                for j, sub_ability in enumerate(ability):
                    if isinstance(sub_ability, dict) and ("cooldown" in sub_ability or "sneakCooldown" in sub_ability):
                        if not found:
                            lines.append("\t#Cooldowns")
                            found = True
                        lines.append(f"\tscoreboard players reset @s {nameShortener(sub_ability.get('name', f'SubAbility{j}'), max_length=12)}{i}CD")
                continue

            if isinstance(ability, dict):
                if ability.get("ultimate"):
                    lines.append("\t#Ultimate")
                    lines.append(f"\tscoreboard players reset @s {ultimate_scoreboard_name(ability.get('name', f'Ability{i}'), i)}")
                    lines.append("")
                    continue

                entries = get_action_slot_entries(ability.get("action_slots", []))
                has_cd = any(e.get("cooldown", 0) > 0 for e in entries)
                if has_cd:
                    lines.append("\t#Cooldowns")
                    lines.append(f"\tscoreboard players reset @s {nameShortener(ability.get('name', f'Ability{i}'), max_length=12)}{i}CD")
            lines.append("\t#User Defined Scoreboards")
            lines.append("")

        return "\n".join(lines)

    lines = [
        f"#Deactivates {characterParams.get('name')}",
        f"tag @s remove {charNameTag}",
        f'tellraw @s [{{"text":"{characterParams.get("name")} deactivated!","color":"{colorCodeHexGen(characterParams.get("color_scheme")[1])}"}}]',
        "",
        delete_ability_item(),
        "",
        "#Deletes Armor",
        *[line for line in delete_armor_line()],
        "",
        "#Clear Effects",
        *[line for line in delete_effects()],
        "",
        reset_scoreboards(),
    ]

    return "\n".join(lines)
