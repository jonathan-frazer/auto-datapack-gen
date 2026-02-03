import os
from constants import charNamespace, characterParams
from utils import get_action_slot_entries
from .ability_utils import ability_namespace, designated_item_json, advancement_json, write_file


def createAdvancementFiles(datapackParams):
    advancement_root = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        datapackParams["namespace"],
        "advancement",
        charNamespace,
    )
    os.makedirs(advancement_root, exist_ok=True)

    abilities = characterParams.get(
        "ability_slots",
        [{"name": "Ability 1"}, {"name": "Ability 2"}, {"name": "Ability 3"}, {"name": "Ability 4"}],
    )

    for i, ability in enumerate(abilities):
        slot_folder = os.path.join(advancement_root, f"slot_{i}")
        os.makedirs(slot_folder, exist_ok=True)

        if isinstance(ability, list):
            designated = designated_item_json(include_model=False)
            path = f"{charNamespace}/slot_{i}/fpress/0_check"
            write_file(os.path.join(slot_folder, "fpress.json"), advancement_json(datapackParams, path, designated))
            continue

        model_name = ability_namespace(ability, f"Ability{i}")
        designated = designated_item_json(include_model=True, model_name=model_name)
        ability_folder = os.path.join(advancement_root, ability_namespace(ability, f"Ability{i}"))
        os.makedirs(ability_folder, exist_ok=True)

        if isinstance(ability, dict):
            if ability.get("ultimate"):
                slot_names = ["f-press"]
            else:
                entries = get_action_slot_entries(ability.get("action_slots", ["f-press", "q-press", "r-click"]))
                slot_names = [e["action"] for e in entries]
                if "f-press" not in slot_names:
                    slot_names.append("f-press")
                if "q-press" not in slot_names:
                    slot_names.append("q-press")

            if "f-press" in slot_names and "shift-f-press" not in slot_names:
                path = f"{charNamespace}/slot_{i}/fpress/0_check"
                write_file(os.path.join(ability_folder, "fpress.json"), advancement_json(datapackParams, path, designated))

            if "f-press" in slot_names and "shift-f-press" in slot_names:
                path = f"{charNamespace}/slot_{i}/fpress/0_check"
                write_file(
                    os.path.join(ability_folder, "fpress.json"),
                    advancement_json(datapackParams, path, designated, sneaking=False),
                )
                path = f"{charNamespace}/slot_{i}/shift_fpress/0_check"
                write_file(
                    os.path.join(ability_folder, "shift_fpress.json"),
                    advancement_json(datapackParams, path, designated, sneaking=True),
                )

            if "shift-f-press" in slot_names and "f-press" not in slot_names:
                path = f"{charNamespace}/slot_{i}/shift_fpress/0_check"
                write_file(
                    os.path.join(ability_folder, "shift_fpress.json"),
                    advancement_json(datapackParams, path, designated, sneaking=True),
                )
