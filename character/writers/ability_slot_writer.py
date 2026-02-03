import os
from constants import ITEM_CUSTOM_DATA_COMPONENT, charNameTag, charNamespace,characterParams
from collections import deque
from utils import nameShortener, colorCodeHexGen, get_action_slot_entries

def createAdvancementFiles(datapackParams):
		advancement_file_path = os.path.join(
				os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
				'data', datapackParams['namespace'], 'advancement', charNamespace
		)
		os.makedirs(advancement_file_path, exist_ok=True)

		for i,ability in enumerate(characterParams.get('ability_slots',[{"name":"Ability 1"},{"name":"Ability 2"},{"name":"Ability 3"},{"name":"Ability 4"}])):
				ability_file_path = os.path.join(advancement_file_path, f"slot_{i}")
				os.makedirs(ability_file_path, exist_ok=True)

				if isinstance(ability, list):
						designatedItem = f""""items": "minecraft:warped_fungus_on_a_stick",
							"components": {{
								"minecraft:custom_data": "{{{charNameTag}:1}}"
							}}"""
						with open(os.path.join(ability_file_path,'fpress.json'),'w') as f:
								f.write(f"""{{
	"criteria": {{
		"f_press": {{
			"trigger": "minecraft:inventory_changed",
			"conditions": {{
				"player": {{
					"type": "minecraft:player",
					"equipment": {{
						"offhand": {{
							{designatedItem}
						}}
					}}
				}}
			}}
		}}
	}},
	"rewards": {{
		"function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress/0_check"
	}}
}}""")
						continue

				designatedItem = f""""items": "minecraft:warped_fungus_on_a_stick",
							"components": {{
								"minecraft:custom_data": "{{{charNameTag}:1}}",
								"minecraft:custom_model_data": {{"strings":["{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}"]}}
							}}"""

				ability_file_path = os.path.join(advancement_file_path, (nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name'),type='namespace')))
				os.makedirs(ability_file_path, exist_ok=True)
				if isinstance(ability,dict):
						action_slot_entries = get_action_slot_entries(ability.get('action_slots',['f-press','q-press','r-click']))
						slot_names = [e['action'] for e in action_slot_entries]
						if 'f-press' not in slot_names: slot_names.append('f-press')
						if 'q-press' not in slot_names: slot_names.append('q-press')

						if 'f-press' in slot_names and 'shift-f-press' not in slot_names:
								with open(os.path.join(ability_file_path,'fpress.json'),'w') as f:
										f.write(f"""{{
	"criteria": {{
		"f_press": {{
			"trigger": "minecraft:inventory_changed",
			"conditions": {{
				"player": {{
					"type": "minecraft:player",
					"equipment": {{
						"offhand": {{
							{designatedItem}
						}}
					}}
				}}
			}}
		}}
	}},
	"rewards": {{
		"function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress/0_check"
	}}
}}""")

						if 'f-press' in slot_names and 'shift-f-press' in slot_names:
								with open(os.path.join(ability_file_path,'fpress.json'),'w') as f:
										f.write(f"""{{
	"criteria": {{
		"f_press": {{
			"trigger": "minecraft:inventory_changed",
			"conditions": {{
				"player": {{
					"type": "minecraft:player",
					"flags": {{
						"is_sneaking": false
					}},
					"equipment": {{
						"offhand": {{
							{designatedItem}
						}}
					}}
				}}
			}}
		}}
	}},
	"rewards": {{
		"function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress/0_check"
	}}
}}""")
								with open(os.path.join(ability_file_path,'shift_fpress.json'),'w') as f:
										f.write(f"""{{
	"criteria": {{
		"f_press": {{
			"trigger": "minecraft:inventory_changed",
			"conditions": {{
				"player": {{
					"type": "minecraft:player",
					"flags": {{
						"is_sneaking": true
					}},
					"equipment": {{
						"offhand": {{
							{designatedItem}
						}}
					}}
				}}
			}}
		}}
	}},
	"rewards": {{
		"function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/shift_fpress/0_check"
	}}
}}""")
						
						if 'shift-f-press' in slot_names and 'f-press' not in slot_names:
								with open(os.path.join(ability_file_path,'shift_fpress.json'),'w') as f:
										f.write(f"""{{
	"criteria": {{
		"f_press": {{
			"trigger": "minecraft:inventory_changed",
			"conditions": {{
				"player": {{
					"type": "minecraft:player",
					"flags": {{
						"is_sneaking": true
					}},
					"equipment": {{
						"offhand": {{
							{designatedItem}
						}}
					}}
				}}
			}}
		}}
	}},
	"rewards": {{
		"function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/shift_fpress/0_check"
	}}
}}""")

def createAbilityFiles(datapackParams):
		map = {'r-click':'rclick','q-press':'qpress','shift-click':'shiftclick','shift-q-press':'shift_qpress',
		'f-press':'fpress','shift-f-press':'shift_fpress'}
		colorScheme = characterParams.get('color_scheme',['white'])

		for i,ability in enumerate(characterParams.get('ability_slots',[{"name":"Ability 1","action_slots":["r-click"]},{"name":"Ability 2","action_slots":["r-click"]},{"name":"Ability 3","action_slots":["r-click"]},{"name":"Ability 4","action_slots":["r-click"]}])):
				nameColorIndex = (i//2)%len(colorScheme)
				loreColorIndex = (nameColorIndex+1)%len(colorScheme)

				if isinstance(ability, list):
						#F-Press Check
						fpress_path = os.path.join(
										os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
										'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i}", "fpress", '0_check.mcfunction'
								)
						check_lines = [
											f"#Clean up",
											f"execute if data entity @s SelectedItem.components.\"minecraft:custom_data\".{charNameTag} run item replace entity @s weapon.mainhand with minecraft:air",
											f"execute if data entity @s SelectedItem run item replace entity @s weapon.offhand from entity @s weapon.mainhand",
											f"execute unless data entity @s SelectedItem run item replace entity @s weapon.offhand with minecraft:air",
											"",
											"#Check Slot Number(and Arbitrary Cooldown)",
											f"execute if score @s SelectedSlot matches {i} {f"if score @s {nameShortener(ability.get('name',f"Ability{j}"),max_length=12)}{i}CD matches 0 " if 'cooldown' in ability else ""}run function {datapackParams['namespace']}:{charNamespace}/slot_{i}/cycle",
											f"advancement revoke @s only {datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress"
										]
						os.makedirs(os.path.dirname(fpress_path), exist_ok=True)
						with open(fpress_path, 'w') as f:
								f.write("\n".join(check_lines))

						#Q-Press Check
						qpress_path = os.path.join(
										os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
										'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i}", "qpress", '0_check.mcfunction'
								)
						check_lines = [
											f"#Clean up",
											f"execute positioned ~ ~1 ~ run kill @n[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}},distance=..2]",
											"",
											"#Perform Arbitrary Cooldown Check here",
											f"{f"execute if score @s {nameShortener(ability.get('name',f"Ability{j}"),max_length=12)}{i}CD matches 0 run " if 'cooldown' in ability else ""}function {datapackParams['namespace']}:{charNamespace}/slot_{i}/cycle"
										]
						os.makedirs(os.path.dirname(qpress_path), exist_ok=True)
						with open(qpress_path, 'w') as f:
								f.write("\n".join(check_lines))

						#Cycle Logic
						swapCyclePath = os.path.join(
										os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
										'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i}", "cycle.mcfunction"
								)
						logicLines = [
										f"#F-Press Logic",
										f"execute if entity @s[advancements={{{datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress=true}}] run scoreboard players add @s {nameShortener(charNameTag,max_length=8)}{i}Swap 1",
										f"scoreboard players set @s[scores={{{nameShortener(charNameTag,max_length=8)}{i}Swap={len(ability)}..}}] {nameShortener(charNameTag,max_length=8)}{i}Swap 0",
										"",
										f"#Q-Press Logic",
										f"execute if entity @s[advancements={{{datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress=false}}] run scoreboard players remove @s {nameShortener(charNameTag,max_length=8)}{i}Swap 1",
										f"scoreboard players set @s[scores={{{nameShortener(charNameTag,max_length=8)}{i}Swap=..-1}}] {nameShortener(charNameTag,max_length=8)}{i}Swap {len(ability)-1}",
										"",
										"#Item Replacment"
									]
						#Add Item Replacement Functions
						for j,subAbility in enumerate(ability):
							condition = f"[scores={{{nameShortener(charNameTag,max_length=8)}{i}Swap={j}}}]"
							itemCommand = f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{subAbility if isinstance(subAbility,str) else subAbility.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{subAbility.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(subAbility,type='namespace') if isinstance(subAbility,str) else nameShortener(subAbility.get('name',""),type='namespace')}\"]}}] 1"
							logicLines.append(f"\t#{subAbility if isinstance(subAbility,str) else subAbility.get('name',f"SubAbility {j+1}")}\n\texecute unless data entity @s{condition} Inventory[{{Slot:{i}b}}] run {itemCommand}\n\texecute if data entity @s{condition} Inventory[{{Slot:{i}b}}].components.\"minecraft:custom_data\".{charNameTag} run {itemCommand}\n")
						
						os.makedirs(os.path.dirname(swapCyclePath), exist_ok=True)
						with open(swapCyclePath, 'w') as f:
								f.write("\n".join(logicLines))

						for j,subAbility in enumerate(ability):
							sneakCooldown = subAbility.get('sneakCooldown', 0) if isinstance(subAbility,dict) else 0
							cooldown = subAbility.get('cooldown', 0) if isinstance(subAbility,dict) else 0
	

							#Sneak RClick
							if sneakCooldown > 0:
								lines = [f"say {i}.{j}.{subAbility if isinstance(ability,str) else subAbility.get('name',"SubAbility")}:shift-click",
								f"scoreboard players set @s {nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD {int(sneakCooldown*2)}",
								f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[enchantment_glint_override=true,custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{subAbility if isinstance(subAbility,str) else subAbility.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{subAbility.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(subAbility,type='namespace') if isinstance(subAbility,str) else nameShortener(subAbility.get('name',""),type='namespace')}\"]}}] 1" if sneakCooldown > 0 else ""]
								check_lines = [
											"#Perform Arbitrary Cooldown Check here",
											f"{f"execute if score @s {nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD matches 0 run " if sneakCooldown > 0 else ""}function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(subAbility.get('name',"SubAbility"),max_length=16,type="namespace")}/shiftclick/0_init"
										]

								subAbilityPath = os.path.join(
										os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
										'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i}", f"{j+1}_{nameShortener(subAbility.get('name',"SubAbility"),max_length=16,type="namespace")}" , "shiftclick", '0_init.mcfunction'
								)
								os.makedirs(os.path.dirname(subAbilityPath), exist_ok=True)
								with open(os.path.join(os.path.dirname(subAbilityPath),"0_check.mcfunction"), 'w') as f:
										f.write("\n".join(check_lines))
								with open(subAbilityPath, 'w') as f:
										f.write("\n\n".join(lines))

							#Normal RClick
							lines = [
								f"say {i}.{j}.{subAbility if isinstance(ability,str) else subAbility.get('name',"SubAbility")}:right-click",
								f"{f"scoreboard players set @s {nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD {int(cooldown*2)}" if cooldown > 0 else ""}",
								f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[enchantment_glint_override=true,custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{subAbility if isinstance(subAbility,str) else subAbility.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{subAbility.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(subAbility,type='namespace') if isinstance(subAbility,str) else nameShortener(subAbility.get('name',""),type='namespace')}\"]}}] 1" if cooldown > 0 else ""
							]
							check_lines = [
											"#Perform Arbitrary Cooldown Check here",
											f"{f"execute if score @s {nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD matches 0 run " if cooldown > 0 else ""}function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{j+1}_{nameShortener(subAbility.get('name',"SubAbility"),max_length=16,type="namespace")}/rclick/0_init"
										]

							subAbilityPath = os.path.join(
								os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
								'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i}", f"{j+1}_{nameShortener(subAbility.get('name',"SubAbility"),max_length=16,type="namespace")}" , "rclick", '0_init.mcfunction'
							)
							os.makedirs(os.path.dirname(subAbilityPath), exist_ok=True)
							with open(os.path.join(os.path.dirname(subAbilityPath),"0_check.mcfunction"), 'w') as f:
									f.write("\n".join(check_lines))
							with open(subAbilityPath, 'w') as f:
									f.write("\n\n".join(lines))

							
						continue

				
				if isinstance(ability,dict):
						action_slot_entries = get_action_slot_entries(ability.get('action_slots',['f-press','q-press','r-click']))
						slot_names = [e['action'] for e in action_slot_entries]
						if 'f-press' not in slot_names: action_slot_entries.append({"action": "f-pressNULL", "cooldown": 0})
						if 'q-press' not in slot_names: action_slot_entries.append({"action": "q-pressNULL", "cooldown": 0})

						for entry in action_slot_entries:
								slot = entry['action']
								current_cooldown = entry.get('cooldown', 0)

								lines = [
									f"say {i}.{ability if isinstance(ability,str) else ability.get('name')}:{slot}",
									f"{f"scoreboard players set @s {nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD {int(current_cooldown*2)}" if current_cooldown > 0 else ""}",
									f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[enchantment_glint_override=true,custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{ability if isinstance(ability,str) else ability.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{ability.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}] 1" if current_cooldown > 0 else ""
				 ] if not slot.endswith("NULL") else []
								
								slot = slot.replace('NULL', '')
								ability_file_path = os.path.join(
										os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
										'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i}", f"{map[slot]}", '0_init.mcfunction'
								)
								os.makedirs(os.path.dirname(ability_file_path), exist_ok=True)

								if 'click' in slot:
									check_lines = [
											"#Perform Arbitrary Cooldown Check here",
											f"{f"execute if score @s {nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD matches 0 run " if current_cooldown > 0 else ""}function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{map[slot]}/0_init"
										]
									with open(os.path.join(os.path.dirname(ability_file_path),"0_check.mcfunction"), 'w') as f:
										f.write("\n".join(check_lines))

								if 'q-press' in slot:
										check_lines = [
											f"#Clean up",
											f"execute positioned ~ ~1 ~ run kill @n[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}},distance=..2]",
											f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{ability if isinstance(ability,str) else ability.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{ability.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}] 1",
											"",
											"#Perform Arbitrary Cooldown Check here",
											f"{f"execute if score @s {nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD matches 0 run " if current_cooldown > 0 else ""}function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{map[slot]}/0_init"
										]
										with open(os.path.join(os.path.dirname(ability_file_path),"0_check.mcfunction"), 'w') as f:
											f.write("\n".join(check_lines))
								
								if 'f-press' in slot:
										check_lines = [
											f"#Clean up",
											f"advancement revoke @s only {datapackParams['namespace']}:{charNamespace}/{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name'),type='namespace')}/{map[slot]}",
											f"execute if data entity @s SelectedItem.components.\"minecraft:custom_data\".{charNameTag} run item replace entity @s weapon.mainhand with minecraft:air",
											f"execute if data entity @s SelectedItem run item replace entity @s weapon.offhand from entity @s weapon.mainhand",
											f"execute unless data entity @s SelectedItem run item replace entity @s weapon.offhand with minecraft:air",
											f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{ability if isinstance(ability,str) else ability.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{ability.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}] 1",
											"",
											"#Check Slot Number(and Arbitrary Cooldown)",
											f"execute if score @s SelectedSlot matches {i} {f"if score @s {nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD matches 0 " if current_cooldown > 0 else ""}run function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{map[slot]}/0_init"
										]
										with open(os.path.join(os.path.dirname(ability_file_path),"0_check.mcfunction"), 'w') as f:
											f.write("\n".join(check_lines))

								with open(ability_file_path, 'w') as f:
										f.write("\n\n".join(lines))
