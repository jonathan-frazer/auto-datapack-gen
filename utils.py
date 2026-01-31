def colorCodeHexGen(color):
    color_codes = {
        "black": "#000000",
        "dark_blue": "#0000AA",
        "dark_green": "#00AA00",
        "dark_aqua": "#00AAAA",
        "dark_red": "#AA0000",
        "dark_purple": "#AA00AA",
        "purple": "#C12FFF",
        "gold": "#FFAA00",
        "gray": "#AAAAAA",
        "dark_gray": "#555555",
        "blue": "#5555FF",
        "green": "#55FF55",
        "aqua": "#55FFFF",
        "red": "#FF5555",
        "light_purple": "#FF55FF",
        "yellow": "#FFFF55",
        "white": "#FFFFFF"
    }
    return color_codes.get(color.lower(), color)

def colorCodeIntGen(color):
    color_codes = {
        "black": 0,
        "dark_blue": 0xAA00,
        "dark_green": 0xFF00,
        "dark_aqua": 0xFFFF,
        "dark_red": 0xFF0000,
        "dark_purple": 0xFF00FF,
        "purple": 0xC12FFF,
        "gold": 0xFFFF00,
        "gray": 0xFFFFFF,
        "dark_gray": 0x555555,
        "blue": 0x5555FF,
        "green": 0x55FF55,
        "aqua": 0x55FFFF,
        "red": 0xFF5555,
        "light_purple": 0xFF55FF,
        "yellow": 0xFFFF55,
        "white": 0xFFFFFF
    }
    return color_codes.get(color.lower(), color)

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
