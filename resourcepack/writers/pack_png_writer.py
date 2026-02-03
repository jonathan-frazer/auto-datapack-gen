import os

from resourcepack.texture_generator import write_text_png
from resourcepack.utils import resourcepack_root
from constants import PACKPNG_HEIGHT,PACKPNG_SCALE,PACKPNG_WIDTH


def writePackPng(packParams):
    pack_name = packParams.get("pack_name", "Resource Pack")
    resourcepack_path = resourcepack_root(packParams)
    os.makedirs(resourcepack_path, exist_ok=True)

    resourcepack_png = os.path.join(resourcepack_path, "pack.png")
    write_text_png(resourcepack_png, pack_name, width=PACKPNG_WIDTH, height=PACKPNG_HEIGHT, scale=PACKPNG_SCALE)

    datapack_root = os.path.join(os.getenv("DATAPACK_PATH"), pack_name)
    os.makedirs(datapack_root, exist_ok=True)
    datapack_png = os.path.join(datapack_root, "pack.png")
    write_text_png(datapack_png, pack_name, width=PACKPNG_WIDTH, height=PACKPNG_HEIGHT, scale=PACKPNG_SCALE)
