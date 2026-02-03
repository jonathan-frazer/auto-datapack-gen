import os
import json
import math
from packversion import DatapackMinecraftVersion


def writePackMeta(packParams):
    datapack_file_path = os.path.join(os.getenv("DATAPACK_PATH"), packParams["pack_name"], "pack.mcmeta")
    os.makedirs(os.path.dirname(datapack_file_path), exist_ok=True)

    pack_format = DatapackMinecraftVersion(packParams["minecraft_version"]).pack_format()
    payload = {
        "pack": {
            "description": packParams["description"],
            "pack_format": int(round(pack_format)),
            "min_format": int(math.floor(pack_format)),
            "max_format": int(math.ceil(pack_format)),
        }
    }
    with open(datapack_file_path, "w") as f:
        f.write(json.dumps(payload, indent=4))
