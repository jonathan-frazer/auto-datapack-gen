import os
from ..main_builders import main_file_content, main_halfsec_file_content, main_sec_file_content

def writeMainFile(datapackParams):
    main_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'function', 'main.mcfunction')
    if not os.path.exists(os.path.dirname(main_file_path)):
        os.makedirs(os.path.dirname(main_file_path))
    with open(main_file_path, 'w') as f:
        f.write(main_file_content(datapackParams))

def writeMainHalfSecFile(datapackParams):
    mainhalfsec_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'function', 'main_halfsec.mcfunction')
    if not os.path.exists(os.path.dirname(mainhalfsec_file_path)):
        os.makedirs(os.path.dirname(mainhalfsec_file_path))
    with open(mainhalfsec_file_path, 'w') as f:
        f.write(main_halfsec_file_content(datapackParams))

def writeMainSecFile(datapackParams):
    mainsec_file_path = os.path.join(os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'], 'data', datapackParams['namespace'], 'function', 'main_sec.mcfunction')
    if not os.path.exists(os.path.dirname(mainsec_file_path)):
        os.makedirs(os.path.dirname(mainsec_file_path))
    with open(mainsec_file_path, 'w') as f:
        f.write(main_sec_file_content(datapackParams))