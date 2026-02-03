import os
from ..duration_builders import effect_file_content, quickEffect_file_content, tick_file_content
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


def writeEffectFunction(packParams):
    _write_function(packParams, "effect.mcfunction", effect_file_content(packParams))


def writeQuickEffectFunction(packParams):
    _write_function(packParams, "quick_effect.mcfunction", quickEffect_file_content(packParams))


def writeTickFunction(packParams):
    _write_function(packParams, "tick.mcfunction", tick_file_content(packParams))
