import json
import os

from resourcepack.utils import ability_entries, resourcepack_root


def writeModelFiles(packParams):
    base_path = os.path.join(
        resourcepack_root(packParams),
        "assets",
        "minecraft",
        "models",
        "item",
    )
    os.makedirs(base_path, exist_ok=True)

    for entry in ability_entries():
        payload = {
            "parent": "item/handheld",
            "textures": {"layer0": f"item/{entry['model_name']}"},
        }
        with open(os.path.join(base_path, f"{entry['model_name']}.json"), "w") as handle:
            handle.write(json.dumps(payload, indent=4))
