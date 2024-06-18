from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Orientation

from objects.GameObject import GameObject

# A game object that has velocity

'''

Entity:
    orientation: Orientation
    speed: int

'''
class Entity(GameObject):
    orientation: Orientation
    def __init__(self, game: GameField, x: int, y: int, ori: Orientation, speed: int = 0):
        super().__init__(game, x, y)
        self.orientation = ori
        self.speed = speed