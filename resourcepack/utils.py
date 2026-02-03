import os

from constants import characterParams
from utils import nameShortener


def resourcepack_root(packParams):
    return os.path.join(os.getenv("RESOURCEPACK_PATH"), packParams["pack_name"])


def _ability_display(ability, fallback):
    return ability.get("name", fallback) if isinstance(ability, dict) else str(ability)


def _ability_model(ability, fallback):
    return nameShortener(_ability_display(ability, fallback), type="namespace")


def ability_entries():
    abilities = characterParams.get(
        "ability_slots",
        [{"name": "Ability 1"}, {"name": "Ability 2"}, {"name": "Ability 3"}, {"name": "Ability 4"}],
    )

    entries = []
    seen = set()

    def add_entry(model_name, display_name):
        if model_name in seen:
            return
        seen.add(model_name)
        entries.append({"model_name": model_name, "display_name": display_name})

    for slot_index, ability in enumerate(abilities):
        if isinstance(ability, list):
            for sub_index, sub_ability in enumerate(ability):
                display = _ability_display(sub_ability, f"SubAbility {sub_index}")
                model_name = _ability_model(sub_ability, f"SubAbility{sub_index}")
                add_entry(model_name, display)
            continue

        display = _ability_display(ability, f"Ability{slot_index}")
        model_name = _ability_model(ability, f"Ability{slot_index}")
        add_entry(model_name, display)

    return entries
