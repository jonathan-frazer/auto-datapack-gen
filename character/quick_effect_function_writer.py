import os
from .builders.quick_effect_builder import quickEffect_file_content
from constants import charNamespace

def writeQuickEffectFunction(datapackParams):
    quickEffect_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'function', charNamespace,
        'quick_effect.mcfunction'
    )

    os.makedirs(os.path.dirname(quickEffect_file_path), exist_ok=True)

    with open(quickEffect_file_path, 'w') as f:
        f.write(quickEffect_file_content(datapackParams))