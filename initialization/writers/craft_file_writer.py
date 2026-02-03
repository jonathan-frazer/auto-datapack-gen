import os
from ..craft_builder import craft_file_content
from constants import charNamespace


def writeCraftFile(packParams):
    craft_file_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        f"craft_{charNamespace}.mcfunction",
    )
    os.makedirs(os.path.dirname(craft_file_path), exist_ok=True)
    with open(craft_file_path, "w") as f:
        f.write(craft_file_content())
