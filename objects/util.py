from typing import Literal

Direction = Literal["east", "north", "west", "south"]

def clamp(v, l, h):
    return max(l, min(h, v))