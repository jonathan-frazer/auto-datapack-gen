import os
from constants import ITEM_CUSTOM_DATA_COMPONENT, charNameTag, charNamespace, characterParams
from utils import nameShortener, colorCodeHexGen, get_action_slot_entries, ultimate_scoreboard_name
from .ability_utils import (
    ability_name,
    ability_desc,
    ability_namespace,
    item_command,
    write_file,
)


def _write_list_cycle_files(packParams, slot_index, ability_list, color_scheme, name_color, lore_color):
    fpress_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        charNamespace,
        f"slot_{slot_index}",
        "fpress",
        "0_check.mcfunction",
    )
    fpress_lines = [
        "#Clean up",
        f"execute if data entity @s SelectedItem.components.\"minecraft:custom_data\".{charNameTag} run item replace entity @s weapon.mainhand with minecraft:air",
        "execute if data entity @s SelectedItem run item replace entity @s weapon.offhand from entity @s weapon.mainhand",
        "execute unless data entity @s SelectedItem run item replace entity @s weapon.offhand with minecraft:air",
        "",
        "#Check Slot Number(and Arbitrary Cooldown)",
        f"execute if score @s SelectedSlot matches {slot_index} run function {packParams['namespace']}:{charNamespace}/slot_{slot_index}/cycle",
        f"advancement revoke @s only {packParams['namespace']}:{charNamespace}/slot_{slot_index}/fpress",
    ]
    write_file(fpress_path, "\n".join(fpress_lines))

    qpress_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        charNamespace,
        f"slot_{slot_index}",
        "qpress",
        "0_check.mcfunction",
    )
    qpress_lines = [
        "#Clean up",
        f"execute positioned ~ ~1 ~ run kill @n[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}},distance=..2]",
        "",
        "#Perform Arbitrary Cooldown Check here",
        f"function {packParams['namespace']}:{charNamespace}/slot_{slot_index}/cycle",
    ]
    write_file(qpress_path, "\n".join(qpress_lines))

    cycle_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        charNamespace,
        f"slot_{slot_index}",
        "cycle.mcfunction",
    )
    logic_lines = [
        "#F-Press Logic",
        f"execute if entity @s[advancements={{{packParams['namespace']}:{charNamespace}/slot_{slot_index}/fpress=true}}] run scoreboard players add @s {nameShortener(charNameTag, max_length=8)}{slot_index}Swap 1",
        f"scoreboard players set @s[scores={{{nameShortener(charNameTag, max_length=8)}{slot_index}Swap={len(ability_list)}..}}] {nameShortener(charNameTag, max_length=8)}{slot_index}Swap 0",
        "",
        "#Q-Press Logic",
        f"execute if entity @s[advancements={{{packParams['namespace']}:{charNamespace}/slot_{slot_index}/fpress=false}}] run scoreboard players remove @s {nameShortener(charNameTag, max_length=8)}{slot_index}Swap 1",
        f"scoreboard players set @s[scores={{{nameShortener(charNameTag, max_length=8)}{slot_index}Swap=..-1}}] {nameShortener(charNameTag, max_length=8)}{slot_index}Swap {len(ability_list) - 1}",
        "",
        "#Item Replacment",
    ]

    for j, sub_ability in enumerate(ability_list):
        condition = f"[scores={{{nameShortener(charNameTag, max_length=8)}{slot_index}Swap={j}}}]"
        name = ability_name(sub_ability, f"SubAbility {j+1}")
        desc = ability_desc(sub_ability)
        model = ability_namespace(sub_ability, f"SubAbility{j}")
        base_command = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
        has_cooldown = (
            sub_ability.get("cooldown", 0) or sub_ability.get("sneakCooldown", 0)
            if isinstance(sub_ability, dict)
            else 0
        )
        if has_cooldown:
            cd_name = nameShortener(name, max_length=12)
            ready = f"if score @s {cd_name}{slot_index}CD matches 0 run {base_command}"
            glint = item_command(
                slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True
            )
            cooldown = f"unless score @s {cd_name}{slot_index}CD matches 0 run {glint}"
            logic_lines.append(
                f"\t#{name}\n"
                f"\texecute unless data entity @s{condition} Inventory[{{Slot:{slot_index}b}}] {ready}\n"
                f"\texecute unless data entity @s{condition} Inventory[{{Slot:{slot_index}b}}] {cooldown}\n"
                f"\texecute if data entity @s{condition} Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} {ready}\n"
                f"\texecute if data entity @s{condition} Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} {cooldown}\n"
            )
        else:
            logic_lines.append(
                f"\t#{name}\n"
                f"\texecute unless data entity @s{condition} Inventory[{{Slot:{slot_index}b}}] run {base_command}\n"
                f"\texecute if data entity @s{condition} Inventory[{{Slot:{slot_index}b}}].components.\"minecraft:custom_data\".{charNameTag} run {base_command}\n"
            )

    write_file(cycle_path, "\n".join(logic_lines))

    for j, sub_ability in enumerate(ability_list):
        name = ability_name(sub_ability, "SubAbility")
        desc = ability_desc(sub_ability)
        model = ability_namespace(sub_ability, f"SubAbility{j}")
        sneak_cd = sub_ability.get("sneakCooldown", 0) if isinstance(sub_ability, dict) else 0
        cooldown = sub_ability.get("cooldown", 0) if isinstance(sub_ability, dict) else 0

        if sneak_cd > 0:
            lines = [
                f"say {slot_index}.{j}.{name}:shift-click",
                f"scoreboard players set @s {nameShortener(name, max_length=12)}{slot_index}CD {int(sneak_cd * 2)}",
                item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True),
            ]
            check_lines = [
                "#Perform Arbitrary Cooldown Check here",
                f"execute if score @s {nameShortener(name, max_length=12)}{slot_index}CD matches 0 run function {packParams['namespace']}:{charNamespace}/slot_{slot_index}/{j+1}_{model}/shiftclick/0_init",
            ]
            sub_path = os.path.join(
                os.getenv("DATAPACK_PATH"),
                packParams["pack_name"],
                "data",
                packParams["namespace"],
                "function",
                charNamespace,
                f"slot_{slot_index}",
                f"{j+1}_{model}",
                "shiftclick",
                "0_init.mcfunction",
            )
            write_file(os.path.join(os.path.dirname(sub_path), "0_check.mcfunction"), "\n".join(check_lines))
            write_file(sub_path, "\n\n".join(lines))

        lines = [
            f"say {slot_index}.{j}.{name}:right-click",
            f"scoreboard players set @s {nameShortener(name, max_length=12)}{slot_index}CD {int(cooldown * 2)}"
            if cooldown > 0
            else "",
            item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True)
            if cooldown > 0
            else "",
        ]
        check_lines = [
            "#Perform Arbitrary Cooldown Check here",
            f"{f'execute if score @s {nameShortener(name, max_length=12)}{slot_index}CD matches 0 run ' if cooldown > 0 else ''}function {packParams['namespace']}:{charNamespace}/slot_{slot_index}/{j+1}_{model}/rclick/0_init",
        ]
        sub_path = os.path.join(
            os.getenv("DATAPACK_PATH"),
            packParams["pack_name"],
            "data",
            packParams["namespace"],
            "function",
            charNamespace,
            f"slot_{slot_index}",
            f"{j+1}_{model}",
            "rclick",
            "0_init.mcfunction",
        )
        write_file(os.path.join(os.path.dirname(sub_path), "0_check.mcfunction"), "\n".join(check_lines))
        write_file(sub_path, "\n\n".join(lines))


def _write_ultimate_files(packParams, slot_index, ability, color_scheme, name_color, lore_color):
    ult_score = ultimate_scoreboard_name(ability_name(ability, f"Ability{slot_index}"), slot_index)
    name = ability_name(ability, f"Ability{slot_index}")
    desc = ability_desc(ability)
    model = ability_namespace(ability, f"Ability{slot_index}")
    base_item = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
    glint_item = item_command(slot_index, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True)

    fpress_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        charNamespace,
        f"slot_{slot_index}",
        "fpress",
        "0_check.mcfunction",
    )
    fpress_lines = [
        "#Clean up",
        f"advancement revoke @s only {packParams['namespace']}:{charNamespace}/{ability_namespace(ability, f'Ability{slot_index}')}/fpress",
        f"execute if data entity @s SelectedItem.components.\"minecraft:custom_data\".{charNameTag} run item replace entity @s weapon.mainhand with minecraft:air",
        "execute if data entity @s SelectedItem run item replace entity @s weapon.offhand from entity @s weapon.mainhand",
        "execute unless data entity @s SelectedItem run item replace entity @s weapon.offhand with minecraft:air",
        f"execute if score @s {ult_score} matches ..99 run {glint_item}",
        f"execute if score @s {ult_score} matches 100.. run {base_item}",
        "",
        f"execute if score @s SelectedSlot matches {slot_index} run title @s actionbar [{{\"text\":\"Ultimate: \",\"color\":\"{colorCodeHexGen(color_scheme[name_color])}\"}},{{\"score\":{{\"name\":\"@s\",\"objective\":\"{ult_score}\"}}}},{{\"text\":\"%\",\"color\":\"{colorCodeHexGen(color_scheme[lore_color])}\"}}]",
    ]
    write_file(fpress_path, "\n".join(fpress_lines))

    qpress_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        charNamespace,
        f"slot_{slot_index}",
        "qpress",
        "0_check.mcfunction",
    )
    qpress_lines = [
        "#Clean up",
        f"execute positioned ~ ~1 ~ run kill @n[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}},distance=..2]",
        f"execute if score @s {ult_score} matches ..99 run {glint_item}",
        f"execute if score @s {ult_score} matches 100.. run {base_item}",
        "",
        f"title @s actionbar [{{\"text\":\"Ultimate: \",\"color\":\"{colorCodeHexGen(color_scheme[name_color])}\"}},{{\"score\":{{\"name\":\"@s\",\"objective\":\"{ult_score}\"}}}},{{\"text\":\"%\",\"color\":\"{colorCodeHexGen(color_scheme[lore_color])}\"}}]",
    ]
    write_file(qpress_path, "\n".join(qpress_lines))

    rclick_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        charNamespace,
        f"slot_{slot_index}",
        "rclick",
        "0_init.mcfunction",
    )
    write_file(
        os.path.join(os.path.dirname(rclick_path), "0_check.mcfunction"),
        f"execute if score @s {ult_score} matches 100.. run function {packParams['namespace']}:{charNamespace}/slot_{slot_index}/rclick/0_init",
    )
    write_file(
        rclick_path,
        "\n".join(
            [
                "say ultimate_ability",
                f"scoreboard players set @s {ult_score} 0",
                glint_item,
            ]
        ),
    )


def createAbilityFiles(packParams):
    action_map = {
        "r-click": "rclick",
        "q-press": "qpress",
        "shift-click": "shiftclick",
        "shift-q-press": "shift_qpress",
        "f-press": "fpress",
        "shift-f-press": "shift_fpress",
    }
    color_scheme = characterParams.get("color_scheme", ["white"])
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
        name_color = (i // 2) % len(color_scheme)
        lore_color = (name_color + 1) % len(color_scheme)

        if isinstance(ability, list):
            _write_list_cycle_files(packParams, i, ability, color_scheme, name_color, lore_color)
            continue

        if isinstance(ability, dict) and ability.get("ultimate"):
            _write_ultimate_files(packParams, i, ability, color_scheme, name_color, lore_color)
            continue

        if isinstance(ability, dict):
            entries = get_action_slot_entries(ability.get("action_slots", ["f-press", "q-press", "r-click"]))
            slot_names = [e["action"] for e in entries]
            if "f-press" not in slot_names:
                entries.append({"action": "f-pressNULL", "cooldown": 0})
            if "q-press" not in slot_names:
                entries.append({"action": "q-pressNULL", "cooldown": 0})

            for entry in entries:
                slot = entry["action"]
                current_cd = entry.get("cooldown", 0)
                name = ability_name(ability, f"Ability{i}")
                desc = ability_desc(ability)
                model = ability_namespace(ability, f"Ability{i}")

                lines = []
                if not slot.endswith("NULL"):
                    lines = [
                        f"say {i}.{name}:{slot}",
                        f"scoreboard players set @s {nameShortener(name, max_length=12)}{i}CD {int(current_cd * 2)}"
                        if current_cd > 0
                        else "",
                        item_command(
                            i, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True
                        )
                        if current_cd > 0
                        else "",
                    ]

                slot = slot.replace("NULL", "")
                ability_file_path = os.path.join(
                    os.getenv("DATAPACK_PATH"),
                    packParams["pack_name"],
                    "data",
                    packParams["namespace"],
                    "function",
                    charNamespace,
                    f"slot_{i}",
                    f"{action_map[slot]}",
                    "0_init.mcfunction",
                )

                if "click" in slot:
                    check_lines = [
                        "#Perform Arbitrary Cooldown Check here",
                        f"{f'execute if score @s {nameShortener(name, max_length=12)}{i}CD matches 0 run ' if current_cd > 0 else ''}function {packParams['namespace']}:{charNamespace}/slot_{i}/{action_map[slot]}/0_init",
                    ]
                    write_file(os.path.join(os.path.dirname(ability_file_path), "0_check.mcfunction"), "\n".join(check_lines))

                if "q-press" in slot:
                    base_item = item_command(i, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
                    if current_cd > 0:
                        cd_name = nameShortener(name, max_length=12)
                        glint_item = item_command(
                            i, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True
                        )
                        check_lines = [
                            "#Clean up",
                            f"execute positioned ~ ~1 ~ run kill @n[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}},distance=..2]",
                            f"execute if score @s {cd_name}{i}CD matches 0 run {base_item}",
                            f"execute unless score @s {cd_name}{i}CD matches 0 run {glint_item}",
                            "",
                            "#Perform Arbitrary Cooldown Check here",
                            f"execute if score @s {cd_name}{i}CD matches 0 run function {packParams['namespace']}:{charNamespace}/slot_{i}/{action_map[slot]}/0_init",
                        ]
                    else:
                        check_lines = [
                            "#Clean up",
                            f"execute positioned ~ ~1 ~ run kill @n[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}},distance=..2]",
                            base_item,
                            "",
                            "#Perform Arbitrary Cooldown Check here",
                            f"function {packParams['namespace']}:{charNamespace}/slot_{i}/{action_map[slot]}/0_init",
                        ]
                    write_file(os.path.join(os.path.dirname(ability_file_path), "0_check.mcfunction"), "\n".join(check_lines))

                if "f-press" in slot:
                    base_item = item_command(i, name, desc, model, color_scheme[name_color], color_scheme[lore_color])
                    adv_name = ability_namespace(ability, f"Ability{i}")
                    if current_cd > 0:
                        cd_name = nameShortener(name, max_length=12)
                        glint_item = item_command(
                            i, name, desc, model, color_scheme[name_color], color_scheme[lore_color], glint=True
                        )
                        check_lines = [
                            "#Clean up",
                            f"advancement revoke @s only {packParams['namespace']}:{charNamespace}/{adv_name}/{action_map[slot]}",
                            f"execute if data entity @s SelectedItem.components.\"minecraft:custom_data\".{charNameTag} run item replace entity @s weapon.mainhand with minecraft:air",
                            "execute if data entity @s SelectedItem run item replace entity @s weapon.offhand from entity @s weapon.mainhand",
                            "execute unless data entity @s SelectedItem run item replace entity @s weapon.offhand with minecraft:air",
                            f"execute if score @s {cd_name}{i}CD matches 0 run {base_item}",
                            f"execute unless score @s {cd_name}{i}CD matches 0 run {glint_item}",
                            "",
                            "#Check Slot Number(and Arbitrary Cooldown)",
                            f"execute if score @s SelectedSlot matches {i} if score @s {cd_name}{i}CD matches 0 run function {packParams['namespace']}:{charNamespace}/slot_{i}/{action_map[slot]}/0_init",
                        ]
                    else:
                        check_lines = [
                            "#Clean up",
                            f"advancement revoke @s only {packParams['namespace']}:{charNamespace}/{adv_name}/{action_map[slot]}",
                            f"execute if data entity @s SelectedItem.components.\"minecraft:custom_data\".{charNameTag} run item replace entity @s weapon.mainhand with minecraft:air",
                            "execute if data entity @s SelectedItem run item replace entity @s weapon.offhand from entity @s weapon.mainhand",
                            "execute unless data entity @s SelectedItem run item replace entity @s weapon.offhand with minecraft:air",
                            base_item,
                            "",
                            "#Check Slot Number(and Arbitrary Cooldown)",
                            f"execute if score @s SelectedSlot matches {i} run function {packParams['namespace']}:{charNamespace}/slot_{i}/{action_map[slot]}/0_init",
                        ]
                    write_file(os.path.join(os.path.dirname(ability_file_path), "0_check.mcfunction"), "\n".join(check_lines))

                write_file(ability_file_path, "\n".join(lines))
