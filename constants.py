from utils import nameShortener, colorCodeHexGen
from parameter_assertions import load_character_parameters, load_texture_parameters

characterParams = load_character_parameters("parameters/character_parameters.json")
textureParams = load_texture_parameters("parameters/texture_parameters.json")
charNamespace = nameShortener(characterParams.get('name'),type='namespace')
charNameTag = nameShortener(characterParams.get('name'),type='nametag')

TEXTURE_WIDTH = textureParams["texture"]["width"]
TEXTURE_HEIGHT = textureParams["texture"]["height"]
TEXTURE_SCALE = textureParams["texture"]["scale"]

PACKPNG_WIDTH = textureParams["pack"]["width"]
PACKPNG_HEIGHT = textureParams["pack"]["height"]
PACKPNG_SCALE = textureParams["pack"]["scale"]

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

RCLICK_SCOREBOARD_NAME = nameShortener(characterParams['name'],max_length=8,type='namespace')+"RClick"
QPRESS_SCOREBOARD_NAME = nameShortener(characterParams['name'],max_length=8,type='namespace')+"QPress"


