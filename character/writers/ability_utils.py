import os
from constants import ITEM_CUSTOM_DATA_COMPONENT, charNameTag
from utils import nameShortener, colorCodeHexGen


def ability_name(ability, fallback):
    if isinstance(ability, dict):
        return ability.get("name", fallback)
    return str(ability)


def ability_desc(ability, fallback=""):
    if isinstance(ability, dict):
        return ability.get("description", fallback)
    return fallback


def ability_namespace(ability, fallback):
    name = ability_name(ability, fallback)
    return nameShortener(name, type="namespace")


def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def write_file(path, content):
    ensure_dir(path)
    with open(path, "w") as f:
        f.write(content)


def designated_item_json(include_model, model_name=None):
    if include_model:
        return (
            '"items": "minecraft:warped_fungus_on_a_stick",\n'
            '\t\t\t\t\t\t"components": {\n'
            f'\t\t\t\t\t\t\t"minecraft:custom_data": "{{{charNameTag}:1}}",\n'
            f'\t\t\t\t\t\t\t"minecraft:custom_model_data": {{"strings":["{model_name}"]}}\n'
            "\t\t\t\t\t\t}"
        )
    return (
        '"items": "minecraft:warped_fungus_on_a_stick",\n'
        '\t\t\t\t\t\t"components": {\n'
        f'\t\t\t\t\t\t\t"minecraft:custom_data": "{{{charNameTag}:1}}"\n'
        "\t\t\t\t\t\t}"
    )


def item_command(slot_index, name, desc, model_name, name_color, lore_color, glint=False):
    glint_part = "enchantment_glint_override=true," if glint else ""
    return (
        f"item replace entity @s hotbar.{slot_index} with minecraft:warped_fungus_on_a_stick["
        f"{glint_part}custom_data={ITEM_CUSTOM_DATA_COMPONENT},"
        f'item_name={{"text":"{name}","color":"{colorCodeHexGen(name_color)}"}},'
        f'lore=[{{"text":"{desc}","color":"{colorCodeHexGen(lore_color)}"}}],'
        f'custom_model_data={{strings:["{model_name}"]}}] 1'
    )


def advancement_json(packParams, path, designated_item, sneaking=None):
    flags = ""
    if sneaking is True:
        flags = '\t\t\t\t"flags": {"is_sneaking": true},\n'
    elif sneaking is False:
        flags = '\t\t\t\t"flags": {"is_sneaking": false},\n'

    return (
        "{\n"
        '\t"criteria": {\n'
        '\t\t"f_press": {\n'
        '\t\t\t"trigger": "minecraft:inventory_changed",\n'
        '\t\t\t"conditions": {\n'
        '\t\t\t\t"player": {\n'
        '\t\t\t\t\t"type": "minecraft:player",\n'
        f"{flags}"
        '\t\t\t\t\t"equipment": {\n'
        '\t\t\t\t\t\t"offhand": {\n'
        f"\t\t\t\t\t\t\t{designated_item}\n"
        "\t\t\t\t\t\t}\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t}\n"
        "\t\t\t}\n"
        "\t\t}\n"
        "\t},\n"
        '\t"rewards": {\n'
        f'\t\t"function": "{packParams["namespace"]}:{path}"\n'
        "\t}\n"
        "}"
    )
