import os
from .builders.tick_builder import tick_file_content
from constants import charNamespace

def writeTickFunction(datapackParams):
    tick_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'function', charNamespace,
        'tick.mcfunction'
    )

    os.makedirs(os.path.dirname(tick_file_path), exist_ok=True)

    with open(tick_file_path, 'w') as f:
        f.write(tick_file_content(datapackParams))