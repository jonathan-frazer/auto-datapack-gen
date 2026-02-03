import os
from ..reload_builder import reload_file_content


def writeReloadFile(datapackParams):
    load_file_path = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        datapackParams["namespace"],
        "function",
        "reload.mcfunction",
    )
    os.makedirs(os.path.dirname(load_file_path), exist_ok=True)
    with open(load_file_path, "w") as f:
        f.write(reload_file_content(datapackParams))
