import os
from .builders.deactivate_builder import deactivate_file_content
from constants import charNamespace

def writeDeactivationFunction(datapackParams):
    deactivation_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'function', charNamespace,
        'deactivate.mcfunction'
    )

    os.makedirs(os.path.dirname(deactivation_file_path), exist_ok=True)

    with open(deactivation_file_path, 'w') as f:
        f.write(deactivate_file_content(datapackParams))