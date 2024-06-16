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
    _objects: set[GameObject]
    - the GameObjects currently occupying the cell

    x: int
        - the X position on grid
    y: int
        - the Y position on grid
    
    get_objects(): set[GameObject]
        - returns all GameObjects currently occupying the cell
    
    add_object(object: GameObject):
        - adds a GameObject to cell
    
    remove_object(object: GameObject):
        - removes a GameObject from cell

'''

class Cell():
    _objects: set[GameObject]
    def __init__(self, game: PyxelGrid[Cell], x: int, y: int):
        self._game = game
        self.x = x
        self.y = y

        game[x, y] = self

        self._objects = set()

    def get_objects(self) -> set[GameObject]:
        return self._objects
    
    def add_object(self, object: GameObject):
        self._objects.add(object)
    
    def remove_object(self, object: GameObject):
        self._objects.remove(object)


    
