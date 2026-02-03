import os
from ..main_builders import main_file_content, main_halfsec_file_content, main_sec_file_content


def _write(packParams, filename, content):
    file_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "function",
        filename,
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)


def writeMainFile(packParams):
    _write(packParams, "main.mcfunction", main_file_content(packParams))


def writeMainHalfSecFile(packParams):
    _write(packParams, "main_halfsec.mcfunction", main_halfsec_file_content(packParams))


def writeMainSecFile(packParams):
    _write(packParams, "main_sec.mcfunction", main_sec_file_content(packParams))
