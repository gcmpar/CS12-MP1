from typing import Type, Sequence

from objects.GameObject import GameObject
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.Brick import Brick
from objects.Stone import Stone
from objects.Water import Water
from objects.Forest import Forest
from objects.Home import Home
from objects.Mirror import Mirror

sprites: dict[Type[GameObject], Sequence[tuple[int, int]]] = {
    Tank: [(0, y) for y in range(4)]
        + [(1, y) for y in range(4)] # enemy
        + [(0, y) for y in range(4, 8)] # light
        + [(1, y) for y in range(4, 8)] # armored
    ,
    Bullet: [(2, y) for y in range(4)],
    Brick: [(3, 0), (3, 1)],
    Stone: [(3, 2)],
    Water: [(3, 3)],
    Forest: [(3, 4)],
    Home: [(3, 5)],
    Mirror: [(4, 0), (4, 1)],
    
}