import os
from ..main_builder import main_file_content

def writeMainFile(datapackParams):
    main_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'function', 'main.mcfunction')
    if not os.path.exists(os.path.dirname(main_file_path)):
        os.makedirs(os.path.dirname(main_file_path))
    with open(main_file_path, 'w') as f:
        f.write(main_file_content(datapackParams))