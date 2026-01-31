import os
from .builders.effect_builder import effect_file_content
from constants import charNamespace

def writeEffectFunction(datapackParams):
    effect_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'function', charNamespace,
        'effect.mcfunction'
    )

    os.makedirs(os.path.dirname(effect_file_path), exist_ok=True)

    with open(effect_file_path, 'w') as f:
        f.write(effect_file_content(datapackParams))