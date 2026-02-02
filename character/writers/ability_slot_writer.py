import os
from constants import ITEM_CUSTOM_DATA_COMPONENT, charNameTag, charNamespace,characterParams
from collections import deque
from utils import nameShortener

def createAdvancementFiles(datapackParams):
    advancement_file_path = os.path.join(
        os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
        'data', datapackParams['namespace'], 'advancement', charNamespace
    )

    for i,ability in enumerate(characterParams.get('ability_slots',[{"name":"Ability 1"},{"name":"Ability 2"},{"name":"Ability 3"},{"name":"Ability 4"}])):
        ability_file_path = os.path.join(advancement_file_path, (nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name'),type='namespace')))
        os.makedirs(ability_file_path, exist_ok=True)
        if isinstance(ability,dict):
            action_slots = ability.get('action_slots',[])
            if 'f-press' in action_slots and 'shift-f-press' not in action_slots:
                with open(os.path.join(ability_file_path,'fpress.json'),'w') as f:
                    f.write(f"""{{
  "criteria": {{
    "f_press": {{
      "trigger": "minecraft:inventory_changed",
      "conditions": {{
        "player": {{
          "type": "minecraft:player",
          "nbt": {{
            "SelectedItemSlot": {i}
          }},
          "equipment": {{
            "offhand": {{
              "items": "minecraft:warped_fungus_on_a_stick",
                "components": {{
                "minecraft:custom_data": {{\"{charNameTag}\":1}},
                "minecraft:custom_model": {{\"strings\":[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}
              }}
            }},
          
          }}
        }}
      }}
    }}
  }},
  "rewards": {{
    "function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress/0_init"
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
          "nbt": {{
            "SelectedItemSlot": {i}
          }},
          "flags": {{
            "is_sneaking": false
          }},
          "equipment": {{
            "offhand": {{
              "items": "minecraft:warped_fungus_on_a_stick",
              "components": {{
                "minecraft:custom_data": {{\"{charNameTag}\":1}},
                "minecraft:custom_model": {{\"strings\":[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}
              }}
            }}
          }}
        }}
      }}
    }}
  }},
  "rewards": {{
    "function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/fpress/0_init"
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
          "nbt": {{
            "SelectedItemSlot": {i}
          }},
          "flags": {{
            "is_sneaking": true
          }},
          "equipment": {{
            "offhand": {{
              "items": "minecraft:warped_fungus_on_a_stick",
              "components": {{
                "minecraft:custom_data": {{\"{charNameTag}\":1}},
                "minecraft:custom_model": {{\"strings\":[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}
              }}
            }}
          }}
        }}
      }}
    }}
  }},
  "rewards": {{
    "function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/shift_fpress/0_init"
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
          "nbt": {{
            "SelectedItemSlot": {i}
          }},
          "flags": {{
            "is_sneaking": true
          }},
          "equipment": {{
            "offhand": {{
              "items": "minecraft:warped_fungus_on_a_stick",
              "components": {{
                "minecraft:custom_data": {{\"{charNameTag}\":1}},
                "minecraft:custom_model": {{\"strings\":[\"{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name',""),type='namespace')}\"]}}
              }}
            }}
          }}
        }}
      }}
    }}
  }},
  "rewards": {{
    "function": "{datapackParams['namespace']}:{charNamespace}/slot_{i}/shift_fpress/0_init"
  }}
}}""")

def createAbilityFiles(datapackParams):
    map = {'r-click':'rclick','q-press':'qpress','shift-click':'shiftclick','shift-q-press':'shift_qpress',
    'f-press':'fpress','shift-f-press':'shift_fpress'}

    for i,ability in enumerate(characterParams.get('ability_slots',[{"name":"Ability 1","action_slots":["r-click"]},{"name":"Ability 2","action_slots":["r-click"]},{"name":"Ability 3","action_slots":["r-click"]},{"name":"Ability 4","action_slots":["r-click"]}])):
        if isinstance(ability,dict):
            for slot in ability.get('action_slots'): 
                ability_file_path = os.path.join(
                    os.getenv('DATAPACKS_PATH'), datapackParams['pack_name'],
                    'data', datapackParams['namespace'], 'function', charNamespace, f"slot_{i+1}", f"{map[slot]}", "0_init.mcfunction" 
                )
                os.makedirs(os.path.dirname(ability_file_path), exist_ok=True)

                lines = [f"say {slot}"]
                
                if 'q-press' in slot:
                    lines.append(f"#Kill Thrown Item\nexecute positioned ~ ~1 ~ run kill @n[type=item,nbt={{Item:{{components:{{\"minecraft:custom_data\":{ITEM_CUSTOM_DATA_COMPONENT}}}}}}},distance=..2]")
                
                if 'f-press' in slot:
                    lines.append(f"#Clean up\nadvancement revoke @s only {datapackParams['namespace']}:{charNamespace}/{nameShortener(ability,type='namespace') if isinstance(ability,str) else nameShortener(ability.get('name'),type='namespace')}/{map[slot]}")
                    lines.append(f"item replace entity @s weapon.offhand with air")

                with open(ability_file_path, 'w') as f:
                    f.write("\n\n".join(lines))
            
