from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.GameObject import GameObject
from objects.Item import Item
from objects.Bullet import Bullet

class Home(Item):
    cracked: bool
    def __init__(self, game: GameField, x: int, y: int, cracked: bool = False):
        super().__init__(game, x, y)
        self.cracked = cracked
    
    def collided_with(self, other: GameObject):
        if isinstance(other, Bullet):
            self.destroy()