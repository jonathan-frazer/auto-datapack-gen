def _normalize_color_name(color: str) -> str:
    return color.lower().replace(" ", "_")


def colorCodeHexGen(color):
    if isinstance(color, str):
        color = color.strip()
        # Already a hex code
        if color.startswith("#") and len(color) in (4, 7):
            return color.upper()

    color_codes = {
        # Minecraft base colors
        "black": "#000000",
        "dark_blue": "#0000AA",
        "dark_green": "#00AA00",
        "dark_aqua": "#00AAAA",
        "dark_red": "#AA0000",
        "dark_purple": "#AA00AA",
        "gold": "#FFAA00",
        "gray": "#AAAAAA",
        "dark_gray": "#555555",
        "blue": "#5555FF",
        "green": "#55FF55",
        "aqua": "#55FFFF",
        "red": "#FF5555",
        "light_purple": "#FF55FF",
        "yellow": "#FFFF55",
        "white": "#FFFFFF",
        "purple": "#C12FFF",
        "pink": "#FF77FF",
        "magenta": "#FF00FF",
        "orange": "#FFA500",
        "brown": "#8B4513",
        "cyan": "#00FFFF",
        "lime": "#32CD32",
        "navy": "#000080",
        "teal": "#008080",
        "olive": "#808000",
        "maroon": "#800000",
        "silver": "#C0C0C0",
        "indigo": "#4B0082",
        "violet": "#EE82EE",
        "hot_pink": "#FF00D9",
        "beige": "#F5F5DC",
        "coral": "#FF7F50",
        "salmon": "#FA8072",
        "turquoise": "#40E0D0"
    }

    key = _normalize_color_name(str(color))
    return color_codes.get(key, "#FFFFFF")  # safe fallback


def colorCodeIntGen(color):
    if isinstance(color, int):
        return color

    if isinstance(color, str):
        color = color.strip()
        # Hex string → int
        if color.startswith("#"):
            return int(color[1:], 16)

    color_codes = {
        "black": 0x000000,
        "dark_blue": 0x0000AA,
        "dark_green": 0x00AA00,
        "dark_aqua": 0x00AAAA,
        "dark_red": 0xAA0000,
        "dark_purple": 0xAA00AA,
        "gold": 0xFFAA00,
        "gray": 0xAAAAAA,
        "dark_gray": 0x555555,
        "blue": 0x5555FF,
        "green": 0x55FF55,
        "aqua": 0x55FFFF,
        "red": 0xFF5555,
        "light_purple": 0xFF55FF,
        "yellow": 0xFFFF55,
        "white": 0xFFFFFF,
        "purple": 0xC12FFF,
        "pink": 0xFF77FF,
        "magenta": 0xFF00FF,
        "orange": 0xFFA500,
        "brown": 0x8B4513,
        "cyan": 0x00FFFF,
        "lime": 0x32CD32,
        "navy": 0x000080,
        "teal": 0x008080,
        "olive": 0x808000,
        "maroon": 0x800000,
        "silver": 0xC0C0C0,
        "indigo": 0x4B0082,
        "violet": 0xEE82EE,
        "beige": 0xF5F5DC,
        "hot_pink": 0xFF00D9,
        "coral": 0xFF7F50,
        "salmon": 0xFA8072,
        "turquoise": 0x40E0D0
    }

    key = _normalize_color_name(str(color))
    return color_codes.get(key, 0xFFFFFF)  # safe fallback

def darkenHexColor(color, amount):
    if not color.startswith('#'):
        color = colorCodeHexGen(color)
    color = color.lstrip('#')
    r = max(0, int(color[:2], 16) - amount)
    g = max(0, int(color[2:4], 16) - amount)
    b = max(0, int(color[4:], 16) - amount)
    return f"#{r:02x}{g:02x}{b:02x}"

def brightenHexColor(color, amount):
    if not color.startswith('#'):
        color = colorCodeHexGen(color)
    color = color.lstrip('#')
    r = min(255, int(color[:2], 16) + amount)
    g = min(255, int(color[2:4], 16) + amount)
    b = min(255, int(color[4:], 16) + amount)
    return f"#{r:02x}{g:02x}{b:02x}"

def hexColorToInt(color):
    if not color.startswith('#'):
        color = colorCodeHexGen(color)
    
    color = color.lstrip('#')
    return int(color, 16)

def get_action_slot_entries(action_slots, default_slots=None):
    """
    Normalize action_slots to list of dicts with 'action' and 'cooldown'.
    Supports both old format (list of strings) and new format (list of dicts).
    """
    default_slots = default_slots or ['f-press', 'q-press', 'r-click']
    if not action_slots:
        return [{"action": s, "cooldown": 0} for s in default_slots]
    result = []
    for e in action_slots:
        if isinstance(e, dict):
            result.append({"action": e.get('action', ''), "cooldown": e.get('cooldown', 0)})
        else:
            result.append({"action": str(e), "cooldown": 0})
    return result


def nameShortener( name: str, max_length: int = 16, type: str = "default") -> str:
    # Normalize spacing and capitalization
    words = name
    if type == 'namespace':
        words = name.strip().lower().split()
        separator = '_'
    else: 
        separator = ""
        words = name.strip().title().split()

    if not words:
        return ""

    def join(words_list):
        return separator.join(words_list)

    # Try full name first
    if len(join(words)) <= max_length:
        return join(words)

    # Remove middle words until it fits
    while len(words) > 1:
        if len(words) == 2:
            candidate = join(words)
            if len(candidate) <= max_length:
                return candidate
            break

        middle_index = len(words) // 2
        words.pop(middle_index)

        candidate = join(words)
        if len(candidate) <= max_length:
            return candidate

    # Final fallback: truncate first word
    return words[0][:max_length]

def ultimate_scoreboard_name(ability_name: str, slot_index: int) -> str:
    base = nameShortener(ability_name or f"Ability{slot_index}", max_length=10)
    return f"{base}{slot_index}Ult"
