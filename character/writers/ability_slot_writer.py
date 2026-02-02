import os
from constants import ITEM_CUSTOM_DATA_COMPONENT, charNameTag, charNamespace,characterParams
from collections import deque
from utils import nameShortener,colorCodeHexGen

def createAdvancementFiles(datapackParams):
		advancement_file_path = os.path.join(
				os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
				'data', datapackParams['namespace'], 'advancement', charNamespace
		)



		for i,ability in enumerate(characterParams.get('ability_slots',[{"name":"Ability 1"},{"name":"Ability 2"},{"name":"Ability 3"},{"name":"Ability 4"}])):
				designatedItem = f""""items": "minecraft:warped_fungus_on_a_stick",
							"components": {{
								"minecraft:custom_data": "{{{charNameTag}:1}}",
								"minecraft:custom_model_data": {{"strings":["{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}"]}}
							}}"""

				ability_file_path = os.path.join(advancement_file_path, (nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name'),type='namespace')))
				os.makedirs(ability_file_path, exist_ok=True)
				if isinstance(ability,dict):
						action_slots = ability.get('action_slots',['f-press','q-press','r-click'])[:]
						if 'f-press' not in action_slots: action_slots.append('f-press')
						if 'q-press' not in action_slots: action_slots.append('q-press')

						if 'f-press' in action_slots and 'shift-f-press' not in action_slots:
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

						if 'f-press' in action_slots and 'shift-f-press' in action_slots:
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
						
						if 'shift-f-press' in action_slots and 'f-press' not in action_slots:
								with open(os.path.join(ability_file_path,'shift_fpress.json'),'w') as f:
										f.writef.write(f"""{{
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
				
				if isinstance(ability,dict):
						action_slots = ability.get('action_slots',['f-press','q-press','r-click'])[:]
						if 'f-press' not in action_slots: action_slots.append('f-pressNULL')
						if 'q-press' not in action_slots: action_slots.append('q-pressNULL')

						for slot in action_slots:
								lines = [f"say {i}.{ability if isinstance(ability,str) else ability.get('name')}:{slot}"] if not slot.endswith("NULL") else []
								slot = slot.replace('NULL', '')
								ability_file_path = os.path.join(
										os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
										'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i}", f"{map[slot]}", '0_init.mcfunction'
								)
								os.makedirs(os.path.dirname(ability_file_path), exist_ok=True)

								if 'click' in slot:
									check_lines = [
											"#Perform Arbitrary Cooldown Check here",
											f"execute if entity @s run function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{map[slot]}/0_init"
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
											f"execute if entity @s run function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{map[slot]}/0_init"
										]
										with open(os.path.join(os.path.dirname(ability_file_path),"0_check.mcfunction"), 'w') as f:
											f.write("\n".join(check_lines))
								
								if 'f-press' in slot:
										check_lines = [
											f"#Clean up",
											f"advancement revoke @s only {datapackParams['namespace']}:{charNamespace}/{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name'),type='namespace')}/{map[slot]}",
											f"execute if data entity @s SelectedItem run item replace entity @s weapon.offhand from entity @s weapon.mainhand",
											f"execute unless data entity @s SelectedItem run item replace entity @s weapon.offhand with minecraft:air",
											f"item replace entity @s hotbar.{i} with minecraft:warped_fungus_on_a_stick[custom_data={ITEM_CUSTOM_DATA_COMPONENT},item_name={{\"text\":\"{ability if isinstance(ability,str) else ability.get('name')}\",\"color\":\"{colorCodeHexGen(colorScheme[nameColorIndex])}\"}},lore=[{{\"text\":\"{ability.get('description',"Lorem ipsum dolor sit amet")}\",\"color\":\"{colorCodeHexGen(colorScheme[loreColorIndex])}\"}}],custom_model_data={{strings:[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}] 1",
											"",
											"#Check Slot Number",
											f"execute if score @s SelectedSlot matches {i} run function {datapackParams['namespace']}:{charNamespace}/slot_{i}/{map[slot]}/0_init"
										]
										with open(os.path.join(os.path.dirname(ability_file_path),"0_check.mcfunction"), 'w') as f:
											f.write("\n".join(check_lines))

								with open(ability_file_path, 'w') as f:
										f.write("\n\n".join(lines))