import os
import json

def initializePredicateFiles(datapackParams):
    predicate_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'predicate')
    if not os.path.exists(predicate_file_path):
        os.makedirs(predicate_file_path)

    #Initialize basic predicate files
    for filename in ['is_sneaking.json','is_sprinting.json','is_on_ground.json']:
        with open(os.path.join(predicate_file_path, filename), 'w') as f:
            f.write(json.dumps({
                "condition": "minecraft:entity_properties",
                "entity": "this",
                "predicate": {
                    "type": "minecraft:player",
                    "flags": {
                        filename.split('.')[0]: True
                    }
                }
            }, indent=4))