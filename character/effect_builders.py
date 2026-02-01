from constants import characterParams, ITEM_CUSTOM_DATA_COMPONENT,HIDDEN_COMPONENT,charNameTag
from utils import colorCodeIntGen,colorCodeHexGen

def effect_file_content(datapackParams):
    def generate_armor_line():
        slot_types = ["chest","legs","feet"]
        armor_pieces = ["chestplate","leggings","boots"]

        armor = characterParams.get('armor', [])
        # Pad armor array to ensure it has at least 3 elements, using 'leather' as filler
        padded_armor = list(armor)[:3] + ['leather'] * (3 - len(armor))
        for i in range(3):
            material = padded_armor[i]
            armor_piece = armor_pieces[i]
            slot_type = slot_types[i]
            color = characterParams.get('color_scheme')[(i//2)%len(characterParams.get('color_scheme',[None]))]
            yield f"execute unless data entity @s equipment.{slot_type} run item replace entity @s armor.{slot_type} with {material}_{armor_piece}[{f'dyed_color={colorCodeIntGen(color)},' if material == 'leather' else ''}custom_data={ITEM_CUSTOM_DATA_COMPONENT},unbreakable={{}},item_name={{\"text\":\"{characterParams.get('name').split()[0] + ' ' + armor_piece.title()}\",\"color\":\"{colorCodeHexGen(color)}\"}},tooltip_display={HIDDEN_COMPONENT}] 1\nexecute if data entity @s equipment.{slot_type}.components.\"minecraft:custom_data\".{charNameTag} run item replace entity @s armor.{slot_type} with {material}_{armor_piece}[{f'dyed_color={colorCodeIntGen(color)},' if material == 'leather' else ''}custom_data={ITEM_CUSTOM_DATA_COMPONENT},unbreakable={{}},item_name={{\"text\":\"{characterParams.get('name').split()[0] + ' ' + armor_piece.title()}\",\"color\":\"{colorCodeHexGen(color)}\"}},tooltip_display={HIDDEN_COMPONENT}] 1"

    def generate_effects():
        effects = characterParams.get('effects', [])
        for effect in effects:
            effect_name = effect if isinstance(effect,str) else effect.get('name')
            amplifier = 0 if isinstance(effect,str) else effect.get('amplifier',0)
            yield f"effect give @s minecraft:{effect_name} 2 {amplifier} true"

    lines = [
        "# Runs Every Effect Interval(Sec)",
        "# Armor",
        "\n\n".join(line for line in generate_armor_line()),
        "\n# Effects",
        "\n".join(generate_effects())
    ]

    return "\n".join(lines)

def quickEffect_file_content(datapackParams):
    lines = [
        "# Runs Every Quick Effect Interval(Half Sec)",
        ""
    ]

    return "\n".join(lines)

def tick_file_content(datapackParams):
    lines = [
        "# Runs Every Tick",
        ""
    ]

    return "\n".join(lines)
