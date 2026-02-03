import os


def initializeAdvancementFiles(datapackParams):
    advancement_file_path = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        datapackParams["namespace"],
        "advancement",
        "0.json",
    )
    os.makedirs(os.path.dirname(advancement_file_path), exist_ok=True)
