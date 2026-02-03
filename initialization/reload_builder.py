from constants import QPRESS_SCOREBOARD_NAME, RCLICK_SCOREBOARD_NAME, characterParams, charNameTag
from utils import colorCodeHexGen, nameShortener, get_action_slot_entries, ultimate_scoreboard_name
from collections import deque

def reload_file_content(datapackParams):
	def reload_string_gen():
		message = datapackParams.get('load_msg', 'Datapack Loaded!')
		colorScheme = characterParams.get('color_scheme', ['white'])

		words = message.split()
		formatted_words = []
		for i,word in enumerate(words):
			color = colorScheme[i % len(colorScheme)]
			formatted_words.append(f'{{"text":"{word} ","color":"{colorCodeHexGen(color)}"}}')

		return f'tellraw @a [{",".join(formatted_words)}]'

	def load_scores():
		abilities = characterParams.get('ability_slots',[])
		click = False
		drop = False

		for ability in abilities:
			if isinstance(ability, dict):
				if ability.get('ultimate'):
					click = True
					drop = True
					break
				action_slot_entries = get_action_slot_entries(ability.get('action_slots') or [])
				for entry in action_slot_entries:
					action = entry.get('action', '')
					if not action:
						continue
					if action in ["r-click", "shift-click"]:
						click = True
					if action in ['q-press', 'shift-q-press']:
						drop = True
					if click and drop:
						break

			if click and drop:
				break

		lines = [] 
		abilities = characterParams.get('ability_slots',[])
		for i,ability in enumerate(abilities):
			lines.append(f"#Slot {i+1}")
			if isinstance(ability,list):
				click = True
				drop = True
				lines.append(f"\t#Swap Cycle\n\tscoreboard objectives add {nameShortener(charNameTag,max_length=8)}{i}Swap dummy")
				found = False
				for j,subAbility in enumerate(ability):
					if isinstance(subAbility,dict) and ('cooldown' in subAbility or 'sneakCooldown' in subAbility):
						if not found:
							lines.append("\t#Cooldowns")
							found = True
						lines.append(f"\tscoreboard objectives add {nameShortener(subAbility.get('name',f"SubAbility{j}"),max_length=12)}{i}CD dummy")
				continue
			
			if isinstance(ability, dict):
				if ability.get('ultimate'):
					lines.append("\t#Ultimate")
					lines.append(f"\tscoreboard objectives add {ultimate_scoreboard_name(ability.get('name',f'Ability{i}'), i)} dummy")
					lines.append("")
					continue
				action_slot_entries = get_action_slot_entries(ability.get('action_slots') or [])
				has_cooldown = any((e.get('cooldown') or 0) > 0 for e in action_slot_entries)
				if has_cooldown:
					lines.append("\t#Cooldowns")
					lines.append(f"\tscoreboard objectives add {nameShortener(ability.get('name',f"Ability{i}"),max_length=12)}{i}CD dummy")
			
			lines.append("\t#User Defined Scoreboards")
			lines.append("")
		
		basicLines = [
			f"scoreboard objectives add {RCLICK_SCOREBOARD_NAME} used:warped_fungus_on_a_stick" if click else "",
			f"scoreboard objectives add {QPRESS_SCOREBOARD_NAME} dropped:warped_fungus_on_a_stick" if drop else "",
			f"scoreboard objectives add SelectedSlot dummy"
		]
		lines.append("")
		lines.extend(basicLines)

		return "\n".join(lines)


	lines = [
		"# Runs Once per World Load",
		reload_string_gen(),
		"",
		"# Scoreboards",
		load_scores()
	]

	lines.append(f"\n#Schedule Functions")
	lines.append(f"schedule function {datapackParams['namespace']}:main_sec 1t")
	lines.append(f"schedule function {datapackParams['namespace']}:main_halfsec 1t")

	return "\n".join(lines)
