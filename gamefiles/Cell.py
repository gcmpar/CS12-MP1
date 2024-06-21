from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Item import Item



'''
A container class for all GameObjects

Cell:
    game: GameField
        - reference to game
    _type: Item
        - object that determines cell's type (only one)
    _objects: list[GameObject]
        - the GameObjects currently occupying the cell
    
    x: int
    y: int
    
    get_item() -> Item | None
        - returns current Item
    
    get_objects() -> list[GameObject]
        - returns all GameObjects currently occupying the cell
    
    add_object(obj: GameObject)
    remove_object(obj: GameObject)

'''

class Cell():
    _type: Item | None
    _objects: list[GameObject]
    def __init__(self, game: GameField, x: int, y: int):
        self.game = game
        self.x = x
        self.y = y

        game[y, x] = self

        self._type = None
        self._objects = []

    def get_item(self) -> Item | None:
        return self._type

    def get_objects(self) -> list[GameObject]:
        return self._objects
    
    def add_object(self, obj: GameObject):
        if isinstance(obj, Item):
            if self._type is not None:
                raise ValueError("Cell can only have one Item type!")
            self._type = obj

        if obj in self._objects:
            return
        self._objects.append(obj)
    
    def remove_object(self, obj: GameObject):
        if obj == self._type:
            self._type = None

        if obj not in self._objects:
            return
        self._objects.remove(obj)


    