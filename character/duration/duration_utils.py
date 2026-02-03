from constants import ITEM_CUSTOM_DATA_COMPONENT
from utils import colorCodeHexGen


def item_command(slot_index, name, desc, model_name, name_color, lore_color, glint=False):
    glint_part = "enchantment_glint_override=true," if glint else ""
    return (
        f"item replace entity @s hotbar.{slot_index} with minecraft:warped_fungus_on_a_stick["
        f"{glint_part}custom_data={ITEM_CUSTOM_DATA_COMPONENT},"
        f'item_name={{"text":"{name}","color":"{colorCodeHexGen(name_color)}"}},'
        f'lore=[{{"text":"{desc}","color":"{colorCodeHexGen(lore_color)}"}}],'
        f'custom_model_data={{strings:["{model_name}"]}}] 1'
    )
