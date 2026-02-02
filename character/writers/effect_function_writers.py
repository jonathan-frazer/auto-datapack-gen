import os
from ..duration_builders import effect_file_content, quickEffect_file_content, tick_file_content
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

def writeQuickEffectFunction(datapackParams):
    quickEffect_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'function', charNamespace,
        'quick_effect.mcfunction'
    )

    os.makedirs(os.path.dirname(quickEffect_file_path), exist_ok=True)

    with open(quickEffect_file_path, 'w') as f:
        f.write(quickEffect_file_content(datapackParams))

def writeTickFunction(datapackParams):
    tick_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'function', charNamespace,
        'tick.mcfunction'
    )

    os.makedirs(os.path.dirname(tick_file_path), exist_ok=True)

    with open(tick_file_path, 'w') as f:
        f.write(tick_file_content(datapackParams))