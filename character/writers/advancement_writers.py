import os
from constants import charNamespace,characterParams
from utils import nameShortener

def createAdvancementFiles(datapackParams):
    advancement_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'advancement', charNamespace
    )

    for i,attack in enumerate(characterParams.get('attacks',[{"name":"Attack 1"},{"name":"Attack 2"},{"name":"Attack 3"},{"name":"Attack 4"}])):
        attack_file_path = os.path.join(advancement_file_path, (nameShortener(attack,type='namespace') if isinstance(attack,str) else nameShortener(attack.get('name',type='namespace'))))
        os.makedirs(attack_file_path, exist_ok=True)