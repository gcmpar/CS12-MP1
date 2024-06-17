from typing import Type, Sequence

from objects.GameObject import GameObject
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.Brick import Brick
from objects.Stone import Stone
from objects.Mirror import Mirror

sprites: dict[Type[GameObject], Sequence[tuple[int, int]]] = {
    Tank: [(x, 0) for x in range(4)] + [(x, 1) for x in range(4, 7)],
    Bullet: [(x, 2) for x in range(4)],
    Brick: [(0, 3)],
    Stone: [(1, 3)],
    Mirror: [(0, 4), (1, 4)],

}