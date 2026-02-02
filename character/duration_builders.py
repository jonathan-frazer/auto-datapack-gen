from constants import QPRESS_SCOREBOARD_NAME, RCLICK_SCOREBOARD_NAME, charNamespace, characterParams, ITEM_CUSTOM_DATA_COMPONENT,HIDDEN_COMPONENT,charNameTag
from utils import colorCodeIntGen, colorCodeHexGen, nameShortener, get_action_slot_entries

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

			itemCommand = f"item replace entity @s armor.{slot_type} with {material}_{armor_piece}[{f'dyed_color={colorCodeIntGen(color)},' if material == 'leather' else ''}custom_data={ITEM_CUSTOM_DATA_COMPONENT},unbreakable={{}},item_name={{\"text\":\"{characterParams.get('name').split()[0] + ' ' + armor_piece.title()}\",\"color\":\"{colorCodeHexGen(color)}\"}},tooltip_display={HIDDEN_COMPONENT}] 1"

			yield f"\t#{armor_piece.title()}\n\texecute unless data entity @s equipment.{slot_type} run {itemCommand}\n\texecute if data entity @s equipment.{slot_type}.components.\"minecraft:custom_data\".{charNameTag} run {itemCommand}"

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
	def generate_ability_item():
		colorScheme = characterParams.get('color_scheme',['white'])
		for i,ability in enumerate(characterParams.get('ability_slots',[{"name":"Ability 1"},{"name":"Ability 2"},{"name":"Ability 3"},{"name":"Ability 4"}])):
			nameColorIndex = (i//2)%len(colorScheme)
			loreColorIndex = (nameColorIndex+1)%len(colorScheme)

			if isinstance(ability, list):
				multiToolLines = []
				for j,subAbility in enumerate(ability):
					condition = f"[scores={{{nameShortener(charNameTag,max_length=8)}{i}Swap={j}}}]"
					itemCommand = f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{subAbility if isinstance(subAbility,str) else subAbility.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{subAbility.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(subAbility,type='namespace') if isinstance(subAbility,str) else nameShortener(subAbility.get('name',""),type='namespace')}\"]}}] 1"
					multiToolLines.append(f"\texecute unless data entity @s{condition} Inventory[{{Slot:{i}b}}] run {itemCommand}\n\texecute if data entity @s{condition} Inventory[{{Slot:{i}b}}].components.\"minecraft:custom_data\".{charNameTag} run {itemCommand}")
				yield f"\t#Slot {i}\n{"\n".join(multiToolLines)}" 
				continue
			
			itemCommand = f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{ability if isinstance(ability,str) else ability.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{ability.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}] 1"
			yield f"\t#Slot {i}\n\texecute unless data entity @s Inventory[{{Slot:{i}b}}] run {itemCommand}\n\texecute if data entity @s Inventory[{{Slot:{i}b}}].components.\"minecraft:custom_data\".{charNameTag} run {itemCommand}"

	lines = [
		"# Runs Every Quick Effect Interval(Half Sec)",
		"# Ability Slots",
		"\n\n".join(line for line in generate_ability_item())
	]

	return "\n".join(lines)

def tick_file_content(datapackParams):
	def generateInteractDetectors():
		all_ability_lines = []
		for i, ability in enumerate(characterParams.get('ability_slots', [{"name": "Ability 1", "action_slots": ["r-click"]}, {"name": "Ability 2", "action_slots": ["r-click"]}, {"name": "Ability 3", "action_slots": ["r-click"]}, {"name": "Ability 4", "action_slots": ["r-click"]}])):
			if isinstance(ability, list):
				ability_lines = [
					f"\t#Slot {i+1}",
					f"\texecute if score @s[scores={{SelectedSlot={i}}}] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/qpress/0_check"
				]
				
				for j,subAbility in enumerate(ability):
					ability_lines.append(f"\t\t#{subAbility.get('name',f"SubAbility {j+1}")}")
					if isinstance(subAbility,dict) and subAbility.get('sneakCooldown',0):
						ability_lines.append(f"\t\texecute if score @s[predicate=!{datapackParams['namespace']}:is_sneaking,scores={{SelectedSlot={i},{nameShortener(charNameTag,max_length=8)}{i}Swap={j}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(subAbility.get('name',"SubAbility"),max_length=16,type="namespace")}/rclick/0_check")
						ability_lines.append(f"\t\texecute if score @s[predicate={datapackParams['namespace']}:is_sneaking,scores={{SelectedSlot={i},{nameShortener(charNameTag,max_length=8)}{i}Swap={j}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(subAbility.get('name',"SubAbility"),max_length=16,type="namespace")}/shiftclick/0_check")
					else:
						ability_lines.append(f"\t\texecute if score @s[scores={{SelectedSlot={i},{nameShortener(charNameTag,max_length=8)}{i}Swap={j}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(subAbility.get('name',"SubAbility"),max_length=16,type="namespace")}/rclick/0_check")
					ability_lines.append("")
				ability_lines.append("")

				all_ability_lines.append("\n".join(ability_lines))
				continue

			ability_lines = [f"\t#Slot {i+1}"]
			if isinstance(ability, dict):
				action_slot_entries = get_action_slot_entries(ability.get('action_slots',['f-press','q-press','r-click']))
				slot_names = [e['slot'] for e in action_slot_entries]
				if 'f-press' not in slot_names: slot_names.append('f-press')
				if 'q-press' not in slot_names: slot_names.append('q-press')
				
				# R-Click / Shift-Click Logic
				if "r-click" in slot_names:
					if "shift-click" not in slot_names:
						ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}}] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/rclick/0_check")
					else:
						ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate=!{datapackParams.get('namespace')}:is_sneaking] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/rclick/0_check")
						ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shiftclick/0_check")
				elif "shift-click" in slot_names:
					ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {RCLICK_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shiftclick/0_check")

				# Q-Press / Shift-Q-Press Logic
				if "q-press" in slot_names:
					if "shift-q-press" not in slot_names:
						ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}}] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/qpress/0_check")
					else:
						ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate=!{datapackParams.get('namespace')}:is_sneaking] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/qpress/0_check")
						ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shift_qpress/0_check")
				elif "shift-q-press" in slot_names:
					ability_lines.append(f"\texecute if score @s[scores={{SelectedSlot={i}}},predicate={datapackParams.get('namespace')}:is_sneaking] {QPRESS_SCOREBOARD_NAME} matches 1..3 run function {datapackParams.get('namespace')}:{charNamespace}/slot_{i}/shift_qpress/0_check")
			all_ability_lines.append("\n".join(ability_lines))
		yield "\n\n".join(all_ability_lines)

	lines = [
		"# Runs Every Tick",
		f"execute store result score @s SelectedSlot run data get entity @s SelectedItemSlot"
		"\n# Ability",
		f"{"\n\n".join(line for line in generateInteractDetectors())}"
	]

	abilities = characterParams.get('ability_slots',[])
	click = False
	drop = False

	for ability in abilities:
		if isinstance(ability, list):
			click = True
			drop = True
			break
		if isinstance(ability,dict):
			action_slot_entries = get_action_slot_entries(ability.get('action_slots', []))
			for entry in action_slot_entries:
				slot = entry['slot']
				if slot in ["r-click","shift-click"]:        click = True
				if slot in ['q-press','shift-q-press']:      drop = True
				if click and drop:
					break

		if click and drop:
			break
	lines.append(f"\nscoreboard players reset @s {RCLICK_SCOREBOARD_NAME}" if click else "")
	lines.append(f"scoreboard players reset @s {QPRESS_SCOREBOARD_NAME}" if drop else "")

	return "\n".join(lines)
