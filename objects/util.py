from typing import Literal

Orientation = Literal["east", "north", "west", "south"]
Team = Literal["player", "enemy"]

def clamp(v, l, h):
    return max(l, min(h, v))