import os
from ..main_sec_builder import main_sec_file_content

def writeMainSecFile(datapackParams):
    mainsec_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'function', 'main_sec.mcfunction')
    if not os.path.exists(os.path.dirname(mainsec_file_path)):
        os.makedirs(os.path.dirname(mainsec_file_path))
    with open(mainsec_file_path, 'w') as f:
        f.write(main_sec_file_content(datapackParams))