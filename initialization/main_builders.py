from constants import characterParams, charNameTag, charNamespace, ITEM_CUSTOM_DATA_COMPONENT
from utils import nameShortener, get_action_slot_entries


def main_file_content(datapackParams):
    lines = [
        "# Runs Every Tick",
        f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/tick",
    ]
    return "\n".join(lines)


def yield_crafting_recipe():
    for item, data in characterParams.get("crafting_recipe", {}).items():
        count = data.get("count", 1) if isinstance(data, dict) else data
        components = []

        if isinstance(data, dict):
            potion = data.get("potion_contents", "")
            if potion:
                potion_id = potion if potion.startswith("minecraft:") else f"minecraft:{potion}"
                components.append(f"\"minecraft:potion_contents\":{{potion:\"{potion_id}\"}}")

        if components:
            yield f'{{Item:{{id:"{item}",count:{count},components:{{{",".join(components)}}}}}}}'
        else:
            yield f'{{Item:{{id:"{item}",count:{count}}}}}'


def main_halfsec_file_content(datapackParams):
    def generate_crafting_string():
        parts = []
        for i, nbt in enumerate(yield_crafting_recipe()):
            if i == 0:
                parts.append(f"execute at @e[type=item,nbt={nbt}]")
            else:
                parts.append(f"if entity @n[type=item,distance=..2,nbt={nbt}]")
        parts.append(f"run function {datapackParams['namespace']}:craft_{charNamespace}")
        return " ".join(parts)

    def decrement_cooldowns():
        lines = []
        found = False
        abilities = characterParams.get("ability_slots", [])
        for i, ability in enumerate(abilities):
            lines.append(f"#Slot {i+1}")
            if isinstance(ability, list):
                for j, sub_ability in enumerate(ability):
                    if isinstance(sub_ability, dict) and ("cooldown" in sub_ability or "sneakCooldown" in sub_ability):
                        if not found:
                            lines.insert(0, "#Decrement Cooldowns")
                            found = True
                        cd_name = nameShortener(sub_ability.get("name", f"SubAbility{j}"), max_length=12)
                        lines.append(f"\texecute as @a[scores={{{cd_name}{i}CD=1..}}] run scoreboard players remove @s {cd_name}{i}CD 1")
                        lines.append(f"\texecute as @a[scores={{{cd_name}{i}CD=..-1}}] run scoreboard players set @s {cd_name}{i}CD 0")
                continue

            if isinstance(ability, dict):
                entries = get_action_slot_entries(ability.get("action_slots") or [])
                has_cd = any((e.get("cooldown") or 0) > 0 for e in entries)
                if has_cd:
                    if not found:
                        lines.insert(0, "#Decrement Cooldowns")
                        found = True
                    cd_name = nameShortener(ability.get("name", f"Ability{i}"), max_length=12)
                    lines.append(f"\texecute as @a[scores={{{cd_name}{i}CD=1..}}] run scoreboard players remove @s {cd_name}{i}CD 1")
                    lines.append(f"\texecute as @a[scores={{{cd_name}{i}CD=..-1}}] run scoreboard players set @s {cd_name}{i}CD 0")

        return "\n".join(lines)

    lines = [
        "# Runs Every Half Second",
        generate_crafting_string(),
        "",
        "# Activation/Deactivation Check",
        f"execute as @a[tag=!{charNameTag},predicate={datapackParams['namespace']}:{charNamespace}/wearing_head] at @s run function {datapackParams['namespace']}:{charNamespace}/activate",
        f"execute as @a[tag={charNameTag},predicate=!{datapackParams['namespace']}:{charNamespace}/wearing_head] at @s run function {datapackParams['namespace']}:{charNamespace}/deactivate",
        "",
        decrement_cooldowns(),
        "",
        "# Effects",
        f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/quick_effect",
        "",
        f"kill @e[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}}]",
        f"schedule function {datapackParams['namespace']}:main_halfsec 10t",
    ]
    return "\n".join(lines)


def main_sec_file_content(datapackParams):
    lines = [
        "# Runs Every Second",
        f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/effect",
        "",
        f"schedule function {datapackParams['namespace']}:main_sec 1s",
    ]
    return "\n".join(lines)
