from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.GameObject import GameObject
    
from objects.Item import Item
from objects.Bullet import Bullet

class Home(Item):
    def touched(self, other: GameObject):
        if isinstance(other, Bullet):
            self.destroy()