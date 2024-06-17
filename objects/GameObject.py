from __future__ import annotations
from collections.abc import Callable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.GameField import GameField
from objects.Cell import Cell

# Base class for all game objects

'''
GameObject
    __game: PyxelGrid[Cell]
        - reference to main game
    _cell: Cell
        - reference to the cell it's currently in
    _on_destroy: list[Callable[[], None]]
    destroyed: bool
        
    get_cell() -> Cell:
        - returns the cell it's in

    move_to(x: int, y: int) -> bool:
        - attempts to move to cell at (x, y)
        - returns False if unsuccessful
    
    bind_to_destroy(f: Callable[[]])
        - bind a function to destroy callback
    unbind_from_destroy(f: Callable[[]])
        - unbinds a function from detroy callback
    destroy():
        - removes the object from game
        - fires functions in _on_destroy

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
    def __init__(self, game: GameField, x: int, y: int):
        self.game = game
        
        self._cell = game[y, x]
        self._cell.add_object(self)
        self._on_destroy = list[Callable[[], None]]()
        self.destroyed = False

        self.move_to(x, y) # immediately trigger collision check on creation
    
    def get_cell(self) -> Cell:
        return self._cell

    def move_to(self, x: int, y: int) -> bool:
        # sanity check
        if not self.game.in_bounds(x, y):
            self.out_of_bounds()
            return False
        
        current_cell = self._cell
        target_cell: Cell = self.game[y, x]
        
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
    
    def bind_to_destroy(self, f: Callable[[], None]):
        if f in self._on_destroy:
            return
        self._on_destroy.append(f)
    def unbind_from_destroy(self, f: Callable[[], None]):
        if f not in self._on_destroy:
            return
        self._on_destroy.remove(f)
    def destroy(self):
        self._cell.remove_object(self)
        self.destroyed = True
        (f() for f in self._on_destroy)
        del self




    def update(self):
        pass

    def can_collide(self, other: GameObject) -> bool:
        return True
    
    def collided_with(self, other: GameObject):
        pass

    def out_of_bounds(self):
        pass
        