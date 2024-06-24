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
    GENERATING = 4

def clamp(v: float, l: float, h: float):
    return max(l, min(h, v))



# maps Orientation to vector
def orientation_to_move_vector(ori: Orientation):
    x_move = 1 if ori == "east" else -1 if ori == "west" else 0
    y_move = 1 if ori == "south" else -1 if ori == "north" else 0
    return (x_move, y_move)



# maps Orientation to reflection vector
_MIRROR_MAP: dict[Orientation, tuple[int, int]] = {
                    "east": (1, 0),
                    "north": (0, -1),
                    "west": (-1, 0),
                    "south": (0, 1)
    }
# maps reflection vector to Orientation (inverse of above)
_MIRROR_MAP_INV: dict[tuple[int, int], Orientation] = {v: k for k, v in _MIRROR_MAP.items()}
def orientation_to_ref_vector(ori: Orientation, ref_ori: ReflectOrientation):
    c = _MIRROR_MAP[ori]
    c = (c[1], c[0])
    if ref_ori == "northeast":
        c = (-c[0], -c[1])
    return _MIRROR_MAP_INV[c]

def flip_orientation(ori: Orientation):
    return "south" if ori == "north" \
    else "north" if ori == "south" \
    else "west" if ori == "east" \
    else "east"
    