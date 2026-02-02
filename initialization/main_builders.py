from collections import deque
from constants import characterParams, charNameTag, charNamespace, ITEM_CUSTOM_DATA_COMPONENT
from utils import hexColorToInt, brightenHexColor, nameShortener, get_action_slot_entries

def main_file_content(datapackParams):
	lines = [
		"# Runs Every Tick",
		f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/tick"
	]

	return "\n".join(lines)

def yield_crafting_recipe():
	for item, data in characterParams.get('crafting_recipe', {}).items():
		count = data.get('count', 1) if isinstance(data, dict) else data

		components = []
			
		potion_component = f"\"minecraft:potion_contents\":{{potion:\"{data.get('potion_contents') if data.get('potion_contents',"").startswith('minecraft:') else "minecraft:"+data.get('potion_contents')}\"}}" if isinstance(data, dict) else ""
		components.append(potion_component)
			
		if all(bool(component) for component in components):
			yield f'{{Item:{{id:"{item}",count:{count},components:{{{",".join(components)}}}}}}}'
		else:
			yield f'{{Item:{{id:"{item}",count:{count}}}}}'

def main_halfsec_file_content(datapackParams):
	def generate_crafting_string():
		craftString = []
		for i,nbt in enumerate(yield_crafting_recipe()):
			if i == 0:  craftString.append(f"execute at @e[type=item,nbt={nbt}]")
			else:   craftString.append(f"if entity @n[type=item,distance=..2,nbt={nbt}]")
		craftString.append(f"run function {datapackParams['namespace']}:craft_{charNamespace}")
		return " ".join(craftString)
	
	def decrementCooldowns():
		lines = deque([])
		found = False

		abilities = characterParams.get('ability_slots',[])
		for i,ability in enumerate(abilities):
			lines.append(f"#Slot {i+1}")
			if isinstance(ability,list):
				for j,subAbility in enumerate(ability):
					if isinstance(subAbility,dict) and ('cooldown' in subAbility or 'sneakCooldown' in subAbility):
						if not found:
							lines.appendleft("#Decrement Cooldowns")
							found = True
						lines.append(f"\texecute as @a[scores={{{nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD=1..}}] run scoreboard players remove @s {nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD 1")
						lines.append(f"\texecute as @a[scores={{{nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD=..-1}}] run scoreboard players set @s {nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD 0")
				continue
			
			if isinstance(ability, dict):
				action_slot_entries = get_action_slot_entries(ability.get('action_slots') or [])
				has_cooldown = any((e.get('cooldown') or 0) > 0 for e in action_slot_entries)
				if has_cooldown:
					if not found:
						lines.appendleft("#Decrement Cooldowns")
						found = True
					lines.append(f"\texecute as @a[scores={{{nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD=1..}}] run scoreboard players remove @s {nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD 1")
					lines.append(f"\texecute as @a[scores={{{nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD=..-1}}] run scoreboard players set @s {nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD 0")

		return "\n".join(lines)

	lines = [
		"# Runs Every Half Second",
		generate_crafting_string(),
		"\n# Activation/Deactivation Check",
		f"execute as @a[tag=!{charNameTag},predicate={datapackParams['namespace']}:{charNamespace}/wearing_head] at @s run function {datapackParams['namespace']}:{charNamespace}/activate",
		f"execute as @a[tag={charNameTag},predicate=!{datapackParams['namespace']}:{charNamespace}/wearing_head] at @s run function {datapackParams['namespace']}:{charNamespace}/deactivate",
		"\n# Effects",
		f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/quick_effect",
		"",
		decrementCooldowns()
	]
	lines.append(f"\nkill @e[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}}]")
	lines.append(f"\nschedule function {datapackParams['namespace']}:main_halfsec 10t")

	return "\n".join(lines)

def main_sec_file_content(datapackParams):
	
	
	lines = [
		"# Runs Every Second",
		f"execute as @a[tag={charNameTag}] run function {datapackParams['namespace']}:{charNamespace}/effect"
		
	]
	lines.append(f"\nschedule function {datapackParams['namespace']}:main_sec 1s")
	return "\n".join(lines)