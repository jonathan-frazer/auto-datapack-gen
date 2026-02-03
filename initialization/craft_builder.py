from constants import (
    characterParams,
    ITEM_NAME_COMPONENT,
    ITEM_LORE_COMPONENT,
    HEAD_CUSTOM_DATA_COMPONENT,
    ITEM_PROFILE_COMPONENT,
)
from .main_builders import yield_crafting_recipe
from utils import hexColorToInt, brightenHexColor, colorCodeHexGen


def craft_file_content():
    def generate_clearing_string():
        return "\n".join(f"kill @n[type=item,distance=..1.5,nbt={nbt}]" for nbt in yield_crafting_recipe())

    def summon_firework(colors=None):
        if colors is None:
            colors = [("white", "white"), ("black", "black")]

        normalized = []
        for primary, fade in colors:
            if not primary.startswith("#"):
                primary = colorCodeHexGen(primary)
            if not fade.startswith("#"):
                fade = colorCodeHexGen(fade)
            normalized.append((primary, fade))

        colors_list = ",".join(str(hexColorToInt(color[0])) for color in normalized)
        fade_colors_list = ",".join(str(hexColorToInt(color[1])) for color in normalized)

        return (
            "summon firework_rocket ~ ~ ~ {"
            "Life:0,"
            "LifeTime:1,"
            "FireworksItem:{"
            "id:\"minecraft:firework_rocket\","
            "count:1,"
            "components:{"
            "\"minecraft:fireworks\":{"
            "explosions:[{"
            "shape:\"small_ball\","
            "has_twinkle:true,"
            f"colors:[{colors_list}],"
            f"fade_colors:[{fade_colors_list}]"
            "}]"
            "}"
            "}"
            "}"
            "}"
        )

    def craft_item():
        return (
            "summon item ~ ~ ~ {"
            "Item:{"
            "id:\"minecraft:player_head\","
            "count:1b,"
            "components:{"
            f"item_name:{ITEM_NAME_COMPONENT},"
            f"lore:{ITEM_LORE_COMPONENT},"
            f"custom_data:{HEAD_CUSTOM_DATA_COMPONENT},"
            f"profile:{ITEM_PROFILE_COMPONENT}"
            "},"
            "}"
            "}"
        )

    lines = [
        generate_clearing_string(),
        "",
        "#Spawn Item",
        summon_firework(colors=[(c, brightenHexColor(c, 20)) for c in characterParams.get("color_scheme")]),
        craft_item(),
    ]
    return "\n".join(lines)
