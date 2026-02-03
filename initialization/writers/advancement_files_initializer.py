import os


def initializeAdvancementFiles(packParams):
    advancement_file_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "advancement",
        "0.json",
    )
    os.makedirs(os.path.dirname(advancement_file_path), exist_ok=True)
