import os
import json


def writeFunctionTags(datapackParams):
    base_path = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        "minecraft",
        "tags",
        "function",
    )
    os.makedirs(base_path, exist_ok=True)

    load_tag_file_path = os.path.join(base_path, "load.json")
    main_tag_file_path = os.path.join(base_path, "tick.json")

    with open(load_tag_file_path, "w") as f_load, open(main_tag_file_path, "w") as f_main:
        f_load.write(json.dumps({"values": [f"{datapackParams['namespace']}:reload"]}, indent=4))
        f_main.write(json.dumps({"values": [f"{datapackParams['namespace']}:main"]}, indent=4))
