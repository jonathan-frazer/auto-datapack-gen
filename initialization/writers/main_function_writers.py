import os
from ..main_builders import main_file_content, main_halfsec_file_content, main_sec_file_content


def _write(datapackParams, filename, content):
    file_path = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        datapackParams["namespace"],
        "function",
        filename,
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)


def writeMainFile(datapackParams):
    _write(datapackParams, "main.mcfunction", main_file_content(datapackParams))


def writeMainHalfSecFile(datapackParams):
    _write(datapackParams, "main_halfsec.mcfunction", main_halfsec_file_content(datapackParams))


def writeMainSecFile(datapackParams):
    _write(datapackParams, "main_sec.mcfunction", main_sec_file_content(datapackParams))
