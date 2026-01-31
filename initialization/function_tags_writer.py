import os
import json

def writeFunctionTags(datapackParams):
    load_tag_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', 'minecraft', 'tags', 'function', 'load.json')
    main_tag_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', 'minecraft', 'tags', 'function', 'tick.json')

    if not os.path.exists(os.path.dirname(load_tag_file_path)):
        os.makedirs(os.path.dirname(load_tag_file_path))

    with open(load_tag_file_path, 'w') as f_load, open(main_tag_file_path, 'w') as f_main:
        f_load.write(json.dumps({"values": [f"{datapackParams['namespace']}:reload"]}, indent=4))
        f_main.write(json.dumps({"values": [f"{datapackParams['namespace']}:main"]}, indent=4))