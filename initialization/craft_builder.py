from constants import characterParams, charNameTag, charNamespace, ITEM_NAME_COMPONENT, ITEM_LORE_COMPONENT, HEAD_CUSTOM_DATA_COMPONENT, ITEM_PROFILE_COMPONENT
from .main_builders import yield_crafting_recipe
from utils import hexColorToInt, brightenHexColor, colorCodeHexGen

def craft_file_content():
    def generate_clearing_string():
        clearString = []
        for nbt in yield_crafting_recipe():
            clearString.append(f"kill @n[type=item,distance=..1.5,nbt={nbt}]")
        
        return "\n".join(clearString)
    
    def summon_firework(colors=None):
        if colors is None:
            colors = [
                ("white", "white"),
                ("black", "black")
            ]
        
        for i in range(len(colors)):
            if (not colors[i][0].startswith("#")) or (not colors[i][1].startswith("#")):
                colors[i] = (colorCodeHexGen(colors[i][0]), colorCodeHexGen(colors[i][1]))

        colors_list = ",".join(
            f"{hexColorToInt(color[0])}" for color in colors
        )
        fade_colors_list = ",".join(
            f"{hexColorToInt(color[1])}" for color in colors
        )

        return (
            f'summon firework_rocket ~ ~ ~ {{'
            f'Life:0,'
            f'LifeTime:1,'
            f'FireworksItem:{{'
                f'id:"minecraft:firework_rocket",'
                f'count:1,'
                f'components:{{'
                    f'"minecraft:fireworks":{{'
                        f'explosions:[{{'
                            f'shape:"small_ball",'
                            f'has_twinkle:true,'
                            f'colors:[{colors_list}],'
                            f'fade_colors:[{fade_colors_list}]'
                        f'}}]'
                    f'}}'
                f'}}'
            f'}}'
            f'}}'
        )
    
    def craft_item():
        return (
            f'summon item ~ ~ ~ {{'
                f'Item:{{'
                    f'id:"minecraft:player_head",'
                    f'count:1b,'
                    f'components:{{'
                        f'item_name:{ITEM_NAME_COMPONENT},'
                        f'lore:{ITEM_LORE_COMPONENT},'
                        f'custom_data:{HEAD_CUSTOM_DATA_COMPONENT},'
                        f'profile:{ITEM_PROFILE_COMPONENT}'
                    f'}},'
                f'}}'
            f'}}'
        )

    
    lines = [
        generate_clearing_string(),
        "\n",
        "#Spawn Item",
        summon_firework(colors=[(c,brightenHexColor(c,20)) for c in characterParams.get('color_scheme')]),
        craft_item()
    ]

    return "\n".join(lines)