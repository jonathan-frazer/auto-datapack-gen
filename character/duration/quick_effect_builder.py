from constants import charNameTag, characterParams
from utils import nameShortener, get_action_slot_entries, ultimate_scoreboard_name
from .duration_utils import item_command


def quickEffect_file_content(packParams):
    def ability_display(ability, fallback):
        return ability.get("name", fallback) if isinstance(ability, dict) else str(ability)

    def ability_desc(ability, fallback=""):
        return ability.get("description", fallback) if isinstance(ability, dict) else fallback

    def ability_model(ability, fallback):
        return nameShortener(ability_display(ability, fallback), type="namespace")

    def ultimate_lines(slot_index, ability, name_color, lore_color):
        ult_score = ultimate_scoreboard_name(ability.get("name", f"Ability{slot_index}"), slot_index)
        name = ability_display(ability, f"Ability{slot_index}")
        desc = ability_desc(ability)
        model = ability_model(ability, f"Ability{slot_index}")
        base_item = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
        glint_item = item_command(
            slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True
        )
        return (
            f"\t#Slot {slot_index}\n"
            f"\texecute if score @s {ult_score} matches ..99 run scoreboard players add @s {ult_score} 1\n"
            f"\texecute if score @s {ult_score} matches 100.. run scoreboard players set @s {ult_score} 100\n"
            f"\texecute if score @s {ult_score} matches 100.. unless data entity @s Inventory[{{Slot:{slot_index}b}}] run {base_item}\n"
            f"\texecute if score @s {ult_score} matches ..99 unless data entity @s Inventory[{{Slot:{slot_index}b}}] run {glint_item}\n"
            f"\texecute if score @s {ult_score} matches 100.. if data entity @s Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} run {base_item}\n"
            f"\texecute if score @s {ult_score} matches ..99 if data entity @s Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} run {glint_item}"
        )

    def multi_tool_lines(slot_index, ability_list, name_color, lore_color):
        lines = []
        for j, sub_ability in enumerate(ability_list):
            name = ability_display(sub_ability, f"SubAbility {j}")
            desc = ability_desc(sub_ability)
            model = ability_model(sub_ability, f"SubAbility{j}")
            has_cd = (
                sub_ability.get("cooldown", 0) or sub_ability.get("sneakCooldown", 0)
                if isinstance(sub_ability, dict)
                else 0
            )
            condition = f"[scores={{{nameShortener(charNameTag, max_length=8)}{slot_index}Swap={j}}}]"
            lines.append(f"\t\t#{name}")
            if has_cd:
                cd_name = nameShortener(name, max_length=12)
                ready = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
                glint = item_command(
                    slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True
                )
                lines.append(
                    f"\t\texecute unless data entity @s{condition} Inventory[{{Slot:{slot_index}b}}] if score @s {cd_name}{slot_index}CD matches 0 run {ready}\n"
                    f"\t\texecute unless data entity @s{condition} Inventory[{{Slot:{slot_index}b}}] unless score @s {cd_name}{slot_index}CD matches 0 run {glint}\n"
                    f"\t\texecute if data entity @s{condition} Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} if score @s {cd_name}{slot_index}CD matches 0 run {ready}\n"
                    f"\t\texecute if data entity @s{condition} Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} unless score @s {cd_name}{slot_index}CD matches 0 run {glint}"
                )
            else:
                item_cmd = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
                lines.append(
                    f"\t\texecute unless data entity @s{condition} Inventory[{{Slot:{slot_index}b}}] run {item_cmd}\n"
                    f"\t\texecute if data entity @s{condition} Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} run {item_cmd}"
                )
        return f"\t#Slot {slot_index}\n" + "\n".join(lines)

    def single_tool_lines(slot_index, ability, name_color, lore_color):
        name = ability_display(ability, f"Ability{slot_index}")
        desc = ability_desc(ability)
        model = ability_model(ability, f"Ability{slot_index}")
        item_cmd = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
        return (
            f"\t#Slot {slot_index}\n"
            f"\texecute unless data entity @s Inventory[{{Slot:{slot_index}b}}] run {item_cmd}\n"
            f"\texecute if data entity @s Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} run {item_cmd}"
        )

    def single_tool_cd_lines(slot_index, ability, name_color, lore_color):
        name = ability_display(ability, f"Ability{slot_index}")
        desc = ability_desc(ability)
        model = ability_model(ability, f"Ability{slot_index}")
        cd_name = nameShortener(name, max_length=12)
        ready = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
        glint = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True)
        return (
            f"\t#Slot {slot_index}\n"
            f"\texecute unless data entity @s Inventory[{{Slot:{slot_index}b}}] if score @s {cd_name}{slot_index}CD matches 0 run {ready}\n"
            f"\texecute unless data entity @s Inventory[{{Slot:{slot_index}b}}] unless score @s {cd_name}{slot_index}CD matches 0 run {glint}\n"
            f"\texecute if data entity @s Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} if score @s {cd_name}{slot_index}CD matches 0 run {ready}\n"
            f"\texecute if data entity @s Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} unless score @s {cd_name}{slot_index}CD matches 0 run {glint}"
        )

    color_scheme = characterParams.get("color_scheme", ["white"])
    abilities = characterParams.get(
        "ability_slots",
        [{"name": "Ability 1"}, {"name": "Ability 2"}, {"name": "Ability 3"}, {"name": "Ability 4"}],
    )

    def generate_ability_item():
        for i, ability in enumerate(abilities):
            name_color = (i // 2) % len(color_scheme)
            lore_color = (name_color + 1) % len(color_scheme)

            if isinstance(ability, list):
                yield multi_tool_lines(i, ability, name_color, lore_color)
                continue

            if isinstance(ability, dict) and ability.get("ultimate"):
                yield ultimate_lines(i, ability, name_color, lore_color)
                continue

            try:
                has_cd = any(("cooldown" in action_slot) for action_slot in ability["action_slots"])
                if not has_cd:
                    raise KeyError
                yield single_tool_cd_lines(i, ability, name_color, lore_color)
            except (KeyError, IndexError, TypeError):
                yield single_tool_lines(i, ability, name_color, lore_color)

    lines = [
        "# Runs Every Quick Effect Interval(Half Sec)",
        "# Ability Slots",
        "\n\n".join(line for line in generate_ability_item()),
    ]

    return "\n".join(lines)
