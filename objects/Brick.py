from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Item import Item
from objects.Bullet import Bullet

class Brick(Item):
    cracked: bool
    def __init__(self, game: GameField, x: int, y: int,
                 cracked: bool = False,
                 
                 pre_added: Callable[[GameObject], bool] | None = None,
                 ):
        self.cracked = cracked
        super().__init__(game=game, x=x, y=y, pre_added=pre_added)
    
    def touched(self, other: GameObject):
        if isinstance(other, Bullet):
            if not self.cracked:
                self.cracked = True
            else:
                self.destroy()
                return