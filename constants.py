import json
from utils import nameShortener, colorCodeHexGen

characterParams = json.loads(open('parameters/character_parameters.json').read())
charNamespace = nameShortener(characterParams.get('name'),type='namespace')
charNameTag = nameShortener(characterParams.get('name'),type='nametag')

ITEM_NAME_COMPONENT = (
            f'{{'
                f'"color":"{colorCodeHexGen(characterParams.get("color_scheme")[0])}",'
                f'"text":"{characterParams.get("name")}"'
            f'}}'
        )
ITEM_LORE_COMPONENT = (
                f'['
                    f'{{"color":"{colorCodeHexGen(characterParams.get("color_scheme")[1])}","text":"{characterParams.get("description", "")}"}}'
                f']'
            )
HEAD_CUSTOM_DATA_COMPONENT = f'{{{charNameTag}:2}}'
ITEM_CUSTOM_DATA_COMPONENT = f'{{{charNameTag}:1}}'
ITEM_PROFILE_COMPONENT = (
    f'{{'
        f'"properties":['
            f'{{'
                f'"name":"textures",'
                f'"value":"{"eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvY2E3Y2E3ZTc0ZjI3Y2I4ZTI0Y2E3Njk0Y2E0ZjI3Y2I4ZTI0Y2E3Njk0Y2E0ZjI3ZjU1ZGIifX19" if characterParams.get("headTexture") is None else characterParams.get("headTexture")}"'
            f'}}'
        f']'
    f'}}'
)
HIDDEN_COMPONENT = '{hidden_components:["dyed_color","attribute_modifiers","unbreakable"]}'
