from __future__ import annotations

from pyxelgrid import PyxelGrid
from objects.Cell import Cell
from objects.util import clamp

# Base class for all game objects

'''
GameObject
    _game: PyxelGrid[Cell]
        - reference to main game
    _cell: Cell
        - reference to the cell it's currently in
    _deleted: bool
        
    get_cell() -> Cell:
        - returns the cell it's in

    move_to(x: int, y: int) -> bool:
        - attempts to move to cell at (x, y)
        - returns False if unsuccessful
    
    delete():
        - removes the object from game
    ---------------------------------
    INTENDED TO BE OVERRIDEN:

    can_collide(other: GameObject) -> bool:
        - returns True if objects collide with each other

    collided_with(other: GameObject):
        - called whenever a GameObject collides with another
        - called on both for each other
    
    out_of_bounds()
        - called whenever the object attempted to move out of bounds

    update()
        - called every game loop
'''
# TODO deletion
# TODO cell types
class GameObject():
    def __init__(self, game: PyxelGrid[Cell], x: int, y: int):
        self._game = game
        self._cell = game[x, y]
        self._cell.add_object(self)
        self.move_to(x, y) # immediately trigger collision check on creation
    
    def get_cell(self) -> Cell:
        return self._cell

    def move_to(self, x: int, y: int) -> bool:
        # sanity check
        if not self._game.in_bounds(x, y):
            self.out_of_bounds()
            return False
        
        current_cell = self._cell
        target_cell: Cell = self._game[x, y]
        
        for obj in target_cell.get_objects():
            if obj == self:
                continue
            if obj.can_collide(self) and self.can_collide(obj):
                self.collided_with(obj)
                obj.collided_with(self)
                return False
        
        current_cell.remove_object(self)
        target_cell.add_object(self)
        self._cell = target_cell

        return True
    
    def delete(self):
        self._cell.remove_object(self)
        self._deleted = True
        del self




    def update(self):
        pass

    def can_collide(self, other: GameObject):
        return True
    
    def collided_with(self, other: GameObject):
        pass

    def out_of_bounds(self):
        pass
        