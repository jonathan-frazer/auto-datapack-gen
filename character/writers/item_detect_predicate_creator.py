import os
from constants import charNamespace, ITEM_PROFILE_COMPONENT


def createItemDetectPredicate(packParams):
    char_pred_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "predicate",
        charNamespace,
        "wearing_head.json",
    )
    os.makedirs(os.path.dirname(char_pred_path), exist_ok=True)

    predicate_json = (
        "{\n"
        '    "condition": "minecraft:entity_properties",\n'
        '    "entity": "this",\n'
        '    "predicate": {\n'
        '        "type": "minecraft:player",\n'
        '        "equipment": {\n'
        '            "head": {\n'
        '                "items": "minecraft:player_head",\n'
        '                "count": 1,\n'
        '                "components": {\n'
        f'                    "minecraft:profile":{ITEM_PROFILE_COMPONENT}\n'
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}"
    )

    with open(char_pred_path, "w") as f:
        f.write(predicate_json)
