# AI Datapack Generator

This project aims to generate datapacks based on AI input.

## Required JSON configuration files

All JSON files live in the `parameters/` directory:

- `parameters/pack_parameters.json`
- `parameters/character_parameters.json`
- `parameters/texture_parameters.json` (optional; defaults are applied if missing)

The validation rules below come from `parameter_assertions.py`.

### 1) `pack_parameters.json`

Defines datapack metadata (name, namespace, description, Minecraft version, and load message) used to build the pack itself and its identity in-game.

Required fields (all must be non-empty strings):

- `pack_name`
- `namespace`
- `description`
- `minecraft_version`
- `load_msg`

Example:

```json
{
  "pack_name": "Blaze Datapack",
  "namespace": "blaze",
  "description": "Adds Blaze the Cat in Minecraft",
  "minecraft_version": "1.21.11",
  "load_msg": "Blaze Datapack Loaded!"
}
```

### 2) `character_parameters.json`

Defines the character’s gameplay configuration (crafting recipe, abilities, colors, armor, and optional effects) that drives the generated functions and assets.

Required fields:

- `name` (non-empty string)
- `crafting_recipe` (object with at least 2 keys)

Optional fields and rules:

- `color_scheme` (list of strings)
  - If omitted or empty, defaults to `["black", "white"]`.
  - If provided with 1 entry, a second `"white"` is added automatically.
- `headTexture` which takes the arbitrary long string that is used in generating custom MC heads. If not provided a default one is used. Try to keep these unique for each character you make as the heads detection is dependant only upon this one value
- `armor` (list of strings)
  - If omitted or empty, defaults to `["leather", "leather", "leather"]`.
  - If fewer than 3 entries, it is padded with `"leather"` until length 3.
- `effects` (list) if provided.
- `ability_slots` (list) if provided
  - Maximum of 9 entries.
  - Each entry must be either:
    - An object (ability), or
    - A list of objects (sub-abilities).
  - Every ability (or sub-ability) object must include a non-empty `name`.
  - If an ability has `"ultimate": true`, it must NOT include `cooldown`, `sneakCooldown`, or `action_slots`.
  - If `action_slots` is present, it must be a list.
  - Each `action_slots` entry must be one of:
    - `"r-click"`, `"shift-click"`, `"q-press"`, `"shift-q-press"`, `"f-press"`, `"shift-f-press"`.
  - If an `action_slots` entry is an object, it must include an `action` string with one of the values above.

`crafting_recipe` rules:

- Must be an object.
- Must have at least 2 keys.
- Every key must be a string that starts with `"minecraft:"`.

Minimal example:

```json
{
  "name": "Blaze",
  "crafting_recipe": {
    "minecraft:blaze_rod": 1,
    "minecraft:gold_ingot": 1
  }
}
```

Expanded example:

```json
{
  "name": "Blaze",
  "color_scheme": ["orange", "yellow"],
  "armor": ["leather", "leather", "leather"],
  "effects": ["minecraft:fire_resistance"],
  "ability_slots": [
    { "name": "Fire Dash", "cooldown": 60 },
    [{ "name": "Flame Burst" }, { "name": "Heat Wave" }],
    { "name": "Inferno", "ultimate": true }
  ],
  "crafting_recipe": {
    "minecraft:blaze_rod": 1,
    "minecraft:gold_ingot": 1
  }
}
```

### 3) `texture_parameters.json` (optional)

Defines the output sizing for generated PNGs (ability textures and pack icons) used by the resourcepack builder; it is optional and defaults are used if the file is missing.

If this file is missing, the defaults below are used.

Structure:

```json
{
  "texture": { "width": 800, "height": 800, "scale": 6 },
  "pack": { "width": 800, "height": 800, "scale": 6 }
}
```

Rules:

- `texture` and `pack` are objects (if provided).
- `width`, `height`, `scale` are positive integers (if provided).
- Any missing field falls back to the defaults shown above.
