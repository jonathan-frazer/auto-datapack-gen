import os
from ..transformation_builders import activate_file_content, deactivate_file_content
from constants import charNamespace


def _write_function(datapackParams, filename, content):
    file_path = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        datapackParams["namespace"],
        "function",
        charNamespace,
        filename,
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)


def writeActivationFunction(datapackParams):
    _write_function(datapackParams, "activate.mcfunction", activate_file_content(datapackParams))


def writeDeactivationFunction(datapackParams):
    _write_function(datapackParams, "deactivate.mcfunction", deactivate_file_content(datapackParams))
