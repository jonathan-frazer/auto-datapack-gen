import os
import json
import math
from packversion import MinecraftVersion


def writePackMeta(datapackParams):
    datapack_file_path = os.path.join(os.getenv("DATAPACKS_PATH"), datapackParams["pack_name"], "pack.mcmeta")
    os.makedirs(os.path.dirname(datapack_file_path), exist_ok=True)

    pack_format = MinecraftVersion(datapackParams["minecraft_version"]).pack_format()
    payload = {
        "pack": {
            "description": datapackParams["description"],
            "pack_format": int(round(pack_format)),
            "min_format": int(math.floor(pack_format)),
            "max_format": int(math.ceil(pack_format)),
        }
    }
    with open(datapack_file_path, "w") as f:
        f.write(json.dumps(payload, indent=4))
