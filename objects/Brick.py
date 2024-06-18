from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.GameObject import GameObject
from objects.CellObject import CellObject
from objects.Bullet import Bullet

class Brick(CellObject):
    def __init__(self, game: GameField, x: int, y: int):
        super().__init__(game, x, y)
    
    def collided_with(self, other: GameObject):
        if isinstance(other, Bullet):
            self.destroy()