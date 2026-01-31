from constants import charNameTag, charNamespace

def main_file_content(datapackParams):
    lines = [
        "# Runs Every Tick",
        f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/tick"
    ]

    return "\n".join(lines)