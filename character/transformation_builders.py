from constants import charNamespace, characterParams, charNameTag, ITEM_CUSTOM_DATA_COMPONENT
from utils import colorCodeHexGen, nameShortener

def activate_file_content(datapackParams):
	def initializeSwapCycles():
		lines = []
		found = True
		abilities = characterParams.get('ability_slots',[])
		for i,ability in enumerate(abilities):
			if isinstance(ability,list):
				if not found:
					lines.append("#Initialize MultiTool Swapping Scores")
					found = True
				lines.append(f"scoreboard players set @s {nameShortener(charNameTag,max_length=8,type='namespace')}{i}Swap 0")
		
		return "\n".join(lines)

	lines = [
		f"# Activates {characterParams.get('name')}",
		f'tellraw @s [{{"text":"{characterParams.get("name")} activated!","color":"{colorCodeHexGen(characterParams.get("color_scheme")[0])}"}}]',
		f"tag @s add {charNameTag}",
		f"\n#Apply Effects\nfunction {datapackParams['namespace']}:{charNamespace}/effect",
		f"",
		f"{initializeSwapCycles()}"
	]
	return "\n".join(lines)

def deactivate_file_content(datapackParams):
	def delete_ability_item():
		if not isinstance(characterParams,dict):
			return ""
		ability_slots = characterParams.get('ability_slots',[])
		return f"#Delete Ability Items\nclear @s minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT}]{f" {len(ability_slots)}" if ability_slots else ""}"
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

	def resetSwapCycles():
		lines = []
		found = False
		abilities = characterParams.get('ability_slots',[])
		for i,ability in enumerate(abilities):
			if isinstance(ability,list):
				if not found:
					lines.append("#Initialize MultiTool Swapping Scores")
					found = True
				lines.append(f"scoreboard players reset @s {nameShortener(charNameTag,max_length=8,type='namespace')}{i}Swap")
		
		return "\n".join(lines)

	lines = [
		f"#Deactivates {characterParams.get('name')}",
		f"tag @s remove {charNameTag}",
		f'tellraw @s [{{"text":"{characterParams.get("name")} deactivated!","color":"{colorCodeHexGen(characterParams.get("color_scheme")[1])}"}}]',
		"",
		delete_ability_item(),
		"\n#Deletes Armor",
		*[line for line in delete_armor_line()],
		"\n#Clear Effects",
		*[line for line in delete_effects()],
		"",
		f"{resetSwapCycles()}"
	]

	return "\n".join(lines)
