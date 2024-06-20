from typing import Type, Sequence

from objects.GameObject import GameObject
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.Brick import Brick
from objects.Stone import Stone
from objects.Water import Water
from objects.Mirror import Mirror

sprites: dict[Type[GameObject], Sequence[tuple[int, int]]] = {
    Tank: [(0, x) for x in range(4)] + [(1, x) for x in range(4)],
    Bullet: [(2, x) for x in range(4)],
    Brick: [(3, 0), (3, 1)],
    Stone: [(3, 2)],
    Water: [(3, 3)],
    Mirror: [(4, 0), (4, 1)],
    
}