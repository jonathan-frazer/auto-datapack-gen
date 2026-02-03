import json
import os


DEFAULT_TEXTURE_PARAMETERS = {
    "texture": {
        "width": 800,
        "height": 800,
        "scale": 6,
    },
    "pack": {
        "width": 800,
        "height": 800,
        "scale": 6,
    },
}


def _load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _assert_non_empty_str(value, field_name):
    assert isinstance(value, str) and value.strip(), f"{field_name} is required and must be a non-empty string"


def validate_datapack_parameters(params):
    required = ["pack_name", "namespace", "description", "minecraft_version", "load_msg"]
    for key in required:
        _assert_non_empty_str(params.get(key), f"datapack_parameters.{key}")
    return params


def validate_character_parameters(params):
    _assert_non_empty_str(params.get("name"), "character_parameters.name")

    color_scheme = params.get("color_scheme")
    if not color_scheme:
        color_scheme = ["black", "white"]
    else:
        assert isinstance(color_scheme, list), "character_parameters.color_scheme must be a list"
        assert all(isinstance(color, str) for color in color_scheme), "character_parameters.color_scheme must be strings"
        if len(color_scheme) == 1:
            color_scheme = [color_scheme[0], "white"]
    params["color_scheme"] = color_scheme

    armor = params.get("armor")
    if not armor:
        armor = ["leather", "leather", "leather"]
    else:
        assert isinstance(armor, list), "character_parameters.armor must be a list"
        assert all(isinstance(piece, str) for piece in armor), "character_parameters.armor must be strings"
        if len(armor) < 3:
            armor = list(armor) + ["leather"] * (3 - len(armor))
    params["armor"] = armor

    if "effects" in params:
        assert isinstance(params["effects"], list), "character_parameters.effects must be a list"

    if "ability_slots" in params:
        ability_slots = params["ability_slots"]
        assert isinstance(ability_slots, list), "character_parameters.ability_slots must be a list"
        assert len(ability_slots) <= 9, "character_parameters.ability_slots can have up to 9 abilities"

        allowed_action_slots = {
            "r-click",
            "shift-click",
            "q-press",
            "shift-q-press",
            "f-press",
            "shift-f-press",
        }

        for ability in ability_slots:
            if isinstance(ability, list):
                for sub_ability in ability:
                    assert isinstance(sub_ability, dict), "sub-abilities must be objects"
                    _assert_non_empty_str(sub_ability.get("name"), "sub-ability.name")
            elif isinstance(ability, dict):
                _assert_non_empty_str(ability.get("name"), "ability.name")
                if ability.get("ultimate") is True:
                    assert "cooldown" not in ability, "ultimate ability cannot have cooldown"
                    assert "sneakCooldown" not in ability, "ultimate ability cannot have sneakCooldown"
                    assert "action_slots" not in ability, "ultimate ability cannot have action_slots"
                if "action_slots" in ability:
                    assert isinstance(
                        ability["action_slots"], list
                    ), "ability.action_slots must be a list when provided"
                    for entry in ability["action_slots"]:
                        if isinstance(entry, dict):
                            action_value = entry.get("action")
                            assert isinstance(
                                action_value, str
                            ), "ability.action_slots action must be a string"
                            assert action_value in allowed_action_slots, (
                                "ability.action_slots action value is invalid. "
                                "Valid values: "
                                "r-click, shift-click, q-press, shift-q-press, f-press, shift-f-press"
                            )
                        else:
                            action_value = str(entry)
                            assert action_value in allowed_action_slots, (
                                "ability.action_slots value is invalid. "
                                "Valid values: "
                                "r-click, shift-click, q-press, shift-q-press, f-press, shift-f-press"
                            )
            else:
                assert False, "ability must be a dict or list of sub-abilities"

    crafting_recipe = params.get("crafting_recipe")
    assert isinstance(crafting_recipe, dict), "character_parameters.crafting_recipe is required and must be an object"
    assert len(crafting_recipe.keys()) >= 2, "character_parameters.crafting_recipe must have at least 2 keys"
    for key in crafting_recipe.keys():
        assert isinstance(key, str) and key.startswith(
            "minecraft:"
        ), "character_parameters.crafting_recipe keys must start with 'minecraft:'"

    return params


def load_character_parameters(path):
    return validate_character_parameters(_load_json(path))


def load_datapack_parameters(path):
    return validate_datapack_parameters(_load_json(path))


def validate_texture_parameters(params):
    validated = {
        "texture": dict(DEFAULT_TEXTURE_PARAMETERS["texture"]),
        "pack": dict(DEFAULT_TEXTURE_PARAMETERS["pack"]),
    }
    if params is None:
        return validated

    assert isinstance(params, dict), "texture_parameters must be an object"
    for section in ("texture", "pack"):
        if section not in params:
            continue
        section_params = params[section]
        assert isinstance(section_params, dict), f"texture_parameters.{section} must be an object"
        for key in ("width", "height", "scale"):
            if key not in section_params:
                continue
            value = section_params[key]
            assert (
                isinstance(value, int) and value > 0
            ), f"texture_parameters.{section}.{key} must be a positive integer"
            validated[section][key] = value

    return validated


def load_texture_parameters(path):
    if not os.path.exists(path):
        return dict(DEFAULT_TEXTURE_PARAMETERS)
    return validate_texture_parameters(_load_json(path))
