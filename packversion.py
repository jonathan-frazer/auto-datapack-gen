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
            self.patch,
        ) == (
            other.major,
            other.minor,
            other.patch,
        )

    def __lt__(self, other):
        if not isinstance(other, MinecraftVersion):
            return NotImplemented
        return (
            self.major,
            self.minor,
            self.patch,
        ) < (
            other.major,
            other.minor,
            other.patch,
        )

    def _pack_format(self, ranges):
        for start, end, pack in ranges:
            if start <= self <= end:
                return pack
        raise ValueError(f"No pack format for version {self}")


class DatapackMinecraftVersion(MinecraftVersion):
    def pack_format(self):
        return self._pack_format(DATAPACK_FORMAT_RANGES)


class ResourcepackMinecraftVersion(MinecraftVersion):
    def pack_format(self):
        return self._pack_format(RESOURCEPACK_FORMAT_RANGES)


DATAPACK_FORMAT_RANGES = [
    (MinecraftVersion("1.21.4"), MinecraftVersion("1.21.4"), 61),
    (MinecraftVersion("1.21.5"), MinecraftVersion("1.21.5"), 71),
    (MinecraftVersion("1.21.6"), MinecraftVersion("1.21.6"), 80),
    (MinecraftVersion("1.21.7"), MinecraftVersion("1.21.8"), 81),
    (MinecraftVersion("1.21.9"), MinecraftVersion("1.21.10"), 88.0),
    (MinecraftVersion("1.21.11"), MinecraftVersion("1.21.11"), 94.1),
]

RESOURCEPACK_FORMAT_RANGES = [
    (MinecraftVersion("1.21.4"), MinecraftVersion("1.21.4"), 46),
    (MinecraftVersion("1.21.5"), MinecraftVersion("1.21.5"), 55),
    (MinecraftVersion("1.21.6"), MinecraftVersion("1.21.6"), 63),
    (MinecraftVersion("1.21.7"), MinecraftVersion("1.21.8"), 64),
    (MinecraftVersion("1.21.9"), MinecraftVersion("1.21.10"), 69.0),
    (MinecraftVersion("1.21.11"), MinecraftVersion("1.21.11"), 75),
]

if __name__ == "__main__":
    dp_v1 = DatapackMinecraftVersion("1.21.10")
    dp_v2 = DatapackMinecraftVersion("1.21.6")
    rp_v1 = ResourcepackMinecraftVersion("1.21.10")
    rp_v2 = ResourcepackMinecraftVersion("1.21.6")

    print(dp_v1 > dp_v2)  # True
    print(dp_v1.pack_format())  # 88.0
    print(dp_v2.pack_format())  # 80
    print(DatapackMinecraftVersion("1.21.4").pack_format())  # 61
    print(rp_v1.pack_format())  # 69.0
    print(rp_v2.pack_format())  # 63
