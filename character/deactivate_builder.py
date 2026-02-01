from constants import ITEM_CUSTOM_DATA_COMPONENT, characterParams, charNameTag
from utils import colorCodeHexGen

def deactivate_file_content(datapackParams):
    def delete_armor_line():
        armor_pieces = ["chestplate","leggings","boots"]
        armor = characterParams.get('armor', [])
        # Pad armor array to ensure it has at least 3 elements, using 'leather' as filler
        padded_armor = list(armor)[:3] + ['leather'] * (3 - len(armor))

        for i in range(3):
            armor_piece = armor_pieces[i]
            material = padded_armor[i]
            yield f"clear @s {material}_{armor_piece}[custom_data={ITEM_CUSTOM_DATA_COMPONENT}]"

    def delete_effects():
        effects = characterParams.get('effects', [])
        for effect in effects:
            effect_name = effect if isinstance(effect,str) else effect.get('name')
            yield f"effect clear @s minecraft:{effect_name}"

    lines = [
        f"# Deactivates {characterParams.get('name')}",
        f"tag @s remove {charNameTag}",
        f'tellraw @s [{{"text":"{characterParams.get("name")} deactivated!","color":"{colorCodeHexGen(characterParams.get("color_scheme")[1])}"}}]',
        "\n#Deletes Armor",
        "\n".join(line for line in delete_armor_line()),
        "\n#Clear Effects",
        "\n".join(line for line in delete_effects())
    ]
    return "\n".join(lines)