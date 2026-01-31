import os
import json
import math
from packversion import MinecraftVersion


def writePackMeta(datapackParams):
    datapack_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'pack.mcmeta')
    if not os.path.exists(os.path.dirname(datapack_file_path)):
        os.makedirs(os.path.dirname(datapack_file_path))
    with open(datapack_file_path, 'w') as f:
        f.write(json.dumps({
            "pack": {
                "description": datapackParams['description'],
                "pack_format": int(round(MinecraftVersion(datapackParams['minecraft_version']).pack_format())),
                "min_format": int(math.floor(MinecraftVersion(datapackParams['minecraft_version']).pack_format())),
                "max_format": int(math.ceil(MinecraftVersion(datapackParams['minecraft_version']).pack_format()))
            }
        }, indent=4))