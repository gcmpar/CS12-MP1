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
from objects.Powerup import Powerup
from objects.Karma import Karma

ASSET_INDEX: dict[Type[GameObject] | str, Sequence[tuple[int, int]]] = {
    Tank: [(0, y) for y in range(4)] # player
        + [(1, y) for y in range(4)] # enemy
        + [(0, y) for y in range(4, 8)] # Light
        + [(1, y) for y in range(4, 8)] # Armored
    ,
    Bullet: [(2, y) for y in range(4)] # orientations
        + [(2, 4)] # midair
    ,
    Brick: [(3, 0), (3, 1)],
    Stone: [(3, 2)],
    Water: [(3, 3)],
    Forest: [(3, 4)],
    Home: [(3, 5)],
    Mirror: [(4, 0), (4, 1)],
    Powerup: [(4, 2)],
    "Spawn": [(5, 0)],
    "EnemySpawn": [(5, 1)],
    "Spawning": [(5, 2)],
    "Explode": [(6, 0), (6, 1)],

    "Mirage": [(4, 4)],










    Karma: [(7, 7)],
    "K": [(4, 6), (4, 7)]
        + [(5, 6), (5, 7)]
        + [(6, 6), (6, 7)]
        + [(4, 5), (5, 5), (6, 5)]
    ,
    
}