import json
import os

from resourcepack.utils import ability_entries, resourcepack_root


def writeItemDefinition(packParams):
    base_path = os.path.join(
        resourcepack_root(packParams),
        "assets",
        "minecraft",
        "items",
    )
    os.makedirs(base_path, exist_ok=True)

    cases = []
    for entry in ability_entries():
        cases.append(
            {
                "when": entry["model_name"],
                "model": {"type": "model", "model": f"item/{entry['model_name']}"},
            }
        )

    payload = {
        "model": {
            "type": "select",
            "property": "custom_model_data",
            "fallback": {"type": "model", "model": "item/warped_fungus_on_a_stick"},
            "cases": cases,
        }
    }

    with open(os.path.join(base_path, "warped_fungus_on_a_stick.json"), "w") as handle:
        handle.write(json.dumps(payload, indent=4))
