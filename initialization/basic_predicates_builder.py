import json

def get_basic_predicate_content(predicate_name):
    return json.dumps({
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {
            "type": "minecraft:player",
            "flags": {
                predicate_name: True
            }
        }
    }, indent=4)