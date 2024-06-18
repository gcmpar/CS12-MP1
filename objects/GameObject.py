from __future__ import annotations
from collections.abc import Callable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.Cell import Cell

# Base class for all game objects

'''
GameObject
    game: GameField
        - reference to main game
    _cell: Cell
        - reference to the cell it's currently in
    _on_move: list[Callable[[], None]]
    _on_destroy: list[Callable[[], None]]
    _destroyed: bool
        
    get_cell() -> Cell:
        - returns the cell it's in

    move_to(x: int, y: int):
        - moves to cell at (x, y)

    bind_to_move(f: Callable[[]])
        - bind a function to move_to callback
    unbind_from_move(f: Callable[[]])
        - unbind a function from move_to callback
    
    bind_to_destroy(f: Callable[[]])
        - bind a function to destroy callback
    unbind_from_destroy(f: Callable[[]])
        - unbind a function from detroy callback
    destroy()
        - removes the object from game
        - fires functions in _on_destroy
    is_destroyed() -> bool
        returns True if destroyed

        
    ---------------------------------
    INTERNALS
        - basically middlemen before the actual overriden method is called

    main_update(frame_count: int)
    main_collided_with(other: GameObject)
    main_touched(other: GameObject)
    

    ---------------------------------
    INTENDED TO BE OVERRIDEN:

    update(frame_count: int)
        - called every game loop

    i love decoupling
    can_collide(other: GameObject) -> bool = True
        - return True if objects collide with each other (can pass through or not)

    collided_with(other: GameObject)
        - called whenever a GameObject collides with another
        - called on both for each other

    touched(other: GameObject)
        - called whenever a GameObject is on the same cell as another
        - called on both for each other
'''

class GameObject():
    _destroyed: bool
    def __init__(self, game: GameField, x: int, y: int):
        self.game = game
        self._destroyed = False
        self._on_move = list[Callable[[], None]]()
        self._on_destroy = list[Callable[[], None]]()

        self._cell = game[y, x]
        self._cell.add_object(self)

    def get_cell(self) -> Cell:
        return self._cell

    def move_to(self, x: int, y: int):
        if self.is_destroyed():
            return
        
        current_cell = self.get_cell()
        target_cell = self.game[y, x]
        
        current_cell.remove_object(self)
        target_cell.add_object(self)
        self._cell = target_cell

        [f() for f in self._on_move]
    
    def bind_to_move(self, f: Callable[[], None]):
        if f in self._on_move:
            return
        self._on_move.append(f)
    def unbind_from_move(self, f: Callable[[], None]):
        if f not in self._on_move:
            return
        self._on_move.remove(f)

    def bind_to_destroy(self, f: Callable[[], None]):
        if f in self._on_destroy:
            return
        self._on_destroy.append(f)
    def unbind_from_destroy(self, f: Callable[[], None]):
        if f not in self._on_destroy:
            return
        self._on_destroy.remove(f)
    def destroy(self):
        if self.is_destroyed():
            return
            
        self._cell.remove_object(self)
        self._destroyed = True
        [f() for f in self._on_destroy]
        del self
    def is_destroyed(self) -> bool:
        return self._destroyed
    
    
    # ---------------------------------
    # internal

    def main_update(self, frame_count: int):
        if self.is_destroyed():
            return
        self.update(frame_count)
    def main_collided_with(self, other: GameObject):
        if self.is_destroyed():
            return
        self.collided_with(other)
    def main_touched(self, other: GameObject):
        if self.is_destroyed():
            return
        self.touched(other)


    # ---------------------------------
    # method overrides

    def update(self, frame_count: int):
        pass

    def can_collide(self, other: GameObject) -> bool:
        return True
    def collided_with(self, other: GameObject):
        pass
    def touched(self, other: GameObject):
        pass

    
        