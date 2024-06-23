from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.GameObject import GameObject
from objects.Item import Item
from objects.Tank import Tank

'''
A collectible Item

Powerup
    type: str
        - descriptor for rendering or other managers
    execute: Callable[[Tank], None]
        - callback for picking up

'''

class Powerup(Item):
    execute: Callable[[Tank], None]
    def __init__(self, game: GameField, x: int, y: int,
                 type: str, execute: Callable[[Tank], None],
                 
                 pre_added: Callable[[GameObject], bool] | None = None,
                 ):
        self.type = type
        self.execute = execute
        super().__init__(game=game, x=x, y=y, pre_added=pre_added)

    def can_collide(self, other: GameObject) -> bool:
        return False
    
    def touched(self, other: GameObject):
        if not isinstance(other, Tank):
            return
        if other.team == "enemy":
            return
        self.execute(other)
        self.destroy()