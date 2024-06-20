from typing import Literal
import enum


Orientation = Literal["east", "north", "west", "south"]
ReflectOrientation = Literal["northeast", "southeast"]
Team = Literal["player", "enemy"]

class GameState(enum.Enum):
    READY = 0
    ONGOING = 1
    WIN = 2
    LOSE = 3

def clamp(v: float, l: float, h: float):
    return max(l, min(h, v))