import os
from .builders.reload_builder import reload_file_content

def writeReloadFile(datapackParams):
    load_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'function', 'reload.mcfunction')
    if not os.path.exists(os.path.dirname(load_file_path)):
        os.makedirs(os.path.dirname(load_file_path))
    with open(load_file_path, 'w') as f:
        f.write(reload_file_content(datapackParams))