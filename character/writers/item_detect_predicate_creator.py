import os
import json
from constants import charNamespace, ITEM_PROFILE_COMPONENT

def createItemDetectPredicate(datapackParams):
    charPredPath = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'predicate', charNamespace,
        'wearing_head.json'
    )

    os.makedirs(os.path.dirname(charPredPath), exist_ok=True)


    predicate_json = f"""
{{
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {{
        "type": "minecraft:player",
        "equipment": {{
            "head": {{
                "items": "minecraft:player_head",
                "count": 1,
                "components": {{
					"minecraft:profile":{ITEM_PROFILE_COMPONENT}
                }}
            }}
        }}
    }}
}}
""".strip()

    with open(charPredPath, "w") as f:
        f.write(predicate_json)