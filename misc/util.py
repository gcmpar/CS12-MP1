from typing import Literal

Orientation = Literal["east", "north", "west", "south"]
ReflectOrientation = Literal["northeast", "southeast"]
Team = Literal["player", "enemy"]

def clamp(v: float, l: float, h: float):
    return max(l, min(h, v))