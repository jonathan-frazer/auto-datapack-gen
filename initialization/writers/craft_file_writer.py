import os
from ..craft_builder import craft_file_content
from constants import charNamespace


def writeCraftFile(datapackParams):
    craft_file_path = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        datapackParams["namespace"],
        "function",
        f"craft_{charNamespace}.mcfunction",
    )
    os.makedirs(os.path.dirname(craft_file_path), exist_ok=True)
    with open(craft_file_path, "w") as f:
        f.write(craft_file_content())
