import os
from ..activate_builder import activate_file_content
from constants import charNamespace

def writeActivationFunction(datapackParams):
    activation_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'function', charNamespace,
        'activate.mcfunction'
    )
    os.makedirs(os.path.dirname(activation_file_path), exist_ok=True)

    with open(activation_file_path, 'w') as f:
        f.write(activate_file_content(datapackParams))