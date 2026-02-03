import os
from ..reload_builder import reload_file_content


def writeReloadFile(packParams):
    load_file_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        "reload.mcfunction",
    )
    os.makedirs(os.path.dirname(load_file_path), exist_ok=True)
    with open(load_file_path, "w") as f:
        f.write(reload_file_content(packParams))
