from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.GameObject import GameObject

from pyxelgrid import PyxelGrid

# A container class for all GameObjects

'''
Cell:
    _game: PyxelGrid[Cell]
        - reference to game
    _objects: list[GameObject]
    - the GameObjects currently occupying the cell

    x: int
        - the X position on grid
    y: int
        - the Y position on grid
    
    get_objects(): list[GameObject]
        - returns all GameObjects currently occupying the cell
    
    add_object(obj: GameObject):
        - adds a GameObject to cell
    
    remove_object(obj: GameObject):
        - removes a GameObject from cell

'''

class Cell():
    _objects: list[GameObject]
    def __init__(self, game: PyxelGrid[Cell], x: int, y: int):
        self.game = game
        self.x = x
        self.y = y

        game[y, x] = self

        self._objects = list()

    def get_objects(self) -> list[GameObject]:
        return self._objects
    
    def add_object(self, obj: GameObject):
        if obj in self._objects:
            return
        self._objects.append(obj)
    
    def remove_object(self, obj: GameObject):
        if obj not in self._objects:
            return
        self._objects.remove(obj)


    
