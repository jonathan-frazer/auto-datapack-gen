import os
from ..main_halfsec_builder import main_halfsec_file_content

def writeMainHalfSecFile(datapackParams):
    mainhalfsec_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'function', 'main_halfsec.mcfunction')
    if not os.path.exists(os.path.dirname(mainhalfsec_file_path)):
        os.makedirs(os.path.dirname(mainhalfsec_file_path))
    with open(mainhalfsec_file_path, 'w') as f:
        f.write(main_halfsec_file_content(datapackParams))