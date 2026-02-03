import os
from ..transformation_builders import activate_file_content, deactivate_file_content
from constants import charNamespace


def _write_function(packParams, filename, content):
    file_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        charNamespace,
        filename,
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)


def writeActivationFunction(packParams):
    _write_function(packParams, "activate.mcfunction", activate_file_content(packParams))


def writeDeactivationFunction(packParams):
    _write_function(packParams, "deactivate.mcfunction", deactivate_file_content(packParams))
