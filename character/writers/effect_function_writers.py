import os
from ..duration_builders import effect_file_content, quickEffect_file_content, tick_file_content
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


def writeEffectFunction(datapackParams):
    _write_function(datapackParams, "effect.mcfunction", effect_file_content(datapackParams))


def writeQuickEffectFunction(datapackParams):
    _write_function(datapackParams, "quick_effect.mcfunction", quickEffect_file_content(datapackParams))


def writeTickFunction(datapackParams):
    _write_function(datapackParams, "tick.mcfunction", tick_file_content(datapackParams))
