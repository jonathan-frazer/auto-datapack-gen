import json
import math
import os

from packversion import ResourcepackMinecraftVersion
from resourcepack.utils import resourcepack_root


def writeResourcepackMeta(packParams):
    base_path = resourcepack_root(packParams)
    os.makedirs(base_path, exist_ok=True)

    pack_format = ResourcepackMinecraftVersion(packParams["minecraft_version"]).pack_format()
    payload = {
        "pack": {
            "description": packParams["description"],
            "pack_format": int(round(pack_format)),
            "min_format": int(math.floor(pack_format)),
            "max_format": int(math.ceil(pack_format)),
        }
    }

    with open(os.path.join(base_path, "pack.mcmeta"), "w") as handle:
        handle.write(json.dumps(payload, indent=4))
