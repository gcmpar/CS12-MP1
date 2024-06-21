from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.GameObject import GameObject



'''
a game object that determines a cell's type
'''

class Item(GameObject):
    def __init__(self, game: GameField, x: int, y: int):
        if type(self) == Item:
            raise ValueError("Superclass cannot be instantiated.")
        super().__init__(game, x, y)