from __future__ import annotations

from pyxelgrid import PyxelGrid
from objects.Cell import Cell

# Base class for all game objects

'''
GameObject
    _game: PyxelGrid[Cell]
        - reference to main game
    _cell: Cell
        - reference to the cell it's currently in
    
    pass_through: bool
        - whether it allows other GameObjects to be in the same cell

    get_cell() -> Cell:
        - returns the cell it's in
    
    move_to(x: int, y: int) -> bool:
        - attempts to move to cell at (x, y)
        - returns False if unsuccessful
    
    collided_with(other: GameObject):
        - called whenever a GameObject collides with another
        - called on both for each other
        - intended to be overridden

'''

class GameObject():
    _game: PyxelGrid[Cell]
    def __init__(self, game: PyxelGrid[Cell], x: int, y: int, pass_through: bool = False):
        self._game = game
        self._cell = game[x, y]

        # error if created at occupied cell
        for obj in self._cell.get_objects():
            if not obj.pass_through:
                raise ValueError("Cell is occupied!")
        self._cell.add_object(self)
        
        self.pass_through = pass_through
    
    def get_cell(self) -> Cell:
        return self._cell
    
    def move_to(self, x: int, y: int) -> bool:
        target_cell: Cell = self._game[x, y]
        if self._cell == target_cell:
            return True
        
        for obj in target_cell.get_objects():
            if not obj.pass_through:
                self.collided_with(obj)
                obj.collided_with(self)
                return False
        
        self._cell.remove_object(self)
        target_cell.add_object(self)
        self._cell = target_cell

        return True

    def collided_with(self, other: GameObject):
        pass
        