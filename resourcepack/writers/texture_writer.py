import os

from resourcepack.texture_generator import write_text_png
from resourcepack.utils import ability_entries, resourcepack_root
from constants import TEXTURE_HEIGHT, TEXTURE_SCALE, TEXTURE_WIDTH


def writeAbilityTextures(packParams):
    base_path = os.path.join(
        resourcepack_root(packParams),
        "assets",
        "minecraft",
        "textures",
        "item",
    )
    os.makedirs(base_path, exist_ok=True)

    for entry in ability_entries():
        texture_path = os.path.join(base_path, f"{entry['model_name']}.png")
        write_text_png(
            texture_path,
            entry["display_name"],
            width=TEXTURE_WIDTH,
            height=TEXTURE_HEIGHT,
            scale=TEXTURE_SCALE,
        )
