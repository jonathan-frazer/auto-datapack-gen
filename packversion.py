from functools import total_ordering

@total_ordering
class MinecraftVersion:
    __slots__ = ("major", "minor", "patch")

    def __init__(self, version: str):
        parts = version.split(".")
        if len(parts) < 2:
            raise ValueError("Invalid Minecraft version")

        self.major = int(parts[0])
        self.minor = int(parts[1])
        self.patch = int(parts[2]) if len(parts) > 2 else 0

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        if not isinstance(other, MinecraftVersion):
            return NotImplemented
        return (
            self.major,
            self.minor,
            self.patch
        ) == (
            other.major,
            other.minor,
            other.patch
        )

    def __lt__(self, other):
        if not isinstance(other, MinecraftVersion):
            return NotImplemented
        return (
            self.major,
            self.minor,
            self.patch
        ) < (
            other.major,
            other.minor,
            other.patch
        )

    # 🔑 Core logic
    def pack_format(self):
        for start, end, pack in PACK_FORMAT_RANGES:
            if start <= self <= end:
                return pack
        raise ValueError(f"No pack format for version {self}")

PACK_FORMAT_RANGES = [
    (MinecraftVersion("1.13"), MinecraftVersion("1.14.4"), 4),
    (MinecraftVersion("1.15"), MinecraftVersion("1.16.1"), 5),
    (MinecraftVersion("1.16.2"), MinecraftVersion("1.16.5"), 6),
    (MinecraftVersion("1.17"), MinecraftVersion("1.17.1"), 7),
    (MinecraftVersion("1.18"), MinecraftVersion("1.18.1"), 8),
    (MinecraftVersion("1.18.2"), MinecraftVersion("1.18.2"), 9),
    (MinecraftVersion("1.19"), MinecraftVersion("1.19.3"), 10),
    (MinecraftVersion("1.19.4"), MinecraftVersion("1.19.4"), 12),
    (MinecraftVersion("1.20"), MinecraftVersion("1.20.1"), 15),
    (MinecraftVersion("1.20.2"), MinecraftVersion("1.20.2"), 18),
    (MinecraftVersion("1.20.3"), MinecraftVersion("1.20.4"), 26),
    (MinecraftVersion("1.20.5"), MinecraftVersion("1.20.6"), 41),
    (MinecraftVersion("1.21"), MinecraftVersion("1.21.1"), 48),
    (MinecraftVersion("1.21.2"), MinecraftVersion("1.21.3"), 57),
    (MinecraftVersion("1.21.4"), MinecraftVersion("1.21.4"), 61),
    (MinecraftVersion("1.21.5"), MinecraftVersion("1.21.5"), 71),
    (MinecraftVersion("1.21.6"), MinecraftVersion("1.21.6"), 80),
    (MinecraftVersion("1.21.7"), MinecraftVersion("1.21.8"), 81),
    (MinecraftVersion("1.21.9"), MinecraftVersion("1.21.10"), 88.0),
    (MinecraftVersion("1.21.11"), MinecraftVersion("1.21.11"), 94.1),
]

if __name__ == "__main__":
    v1 = MinecraftVersion("1.21.10")
    v2 = MinecraftVersion("1.21.6")

    print(v1 > v2)                 # True
    print(v1.pack_format())        # 88.0
    print(v2.pack_format())        # 80
    print(MinecraftVersion("1.20.4").pack_format())  # 26