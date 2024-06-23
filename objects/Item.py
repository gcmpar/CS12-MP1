from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.GameObject import GameObject



'''
a game object that determines a cell's type
'''

class Item(GameObject):
    def __init__(self, game: GameField, x: int, y: int, pre_added: Callable[[GameObject], bool] | None = None):
        if type(self) == Item:
            raise ValueError("Superclass cannot be instantiated.")
        super().__init__(game=game, x=x, y=y, pre_added=pre_added)