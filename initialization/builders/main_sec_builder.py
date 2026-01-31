from constants import charNameTag, charNamespace

def main_sec_file_content(datapackParams):
    lines = [
        "# Runs Every Second",
        f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/effect"
    ]
    lines.append(f"\nkill @e[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{{{charNameTag}:1}}}}}}}}]")
    lines.append(f"\nschedule function {datapackParams['namespace']}:main_sec 1s")
    return "\n".join(lines)