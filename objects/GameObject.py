from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.Cell import Cell

from misc.Signal import Signal

# Base class for all game objects

'''
GameObject
    game: GameField
        - reference to main game
    id: int
        - object id
    _cell: Cell
        - reference to the cell it's currently in
    _destroyed: bool

    onMove: Signal[[int, int], None]
    onCollision: Signal[[GameObject], None]
    onTouched: Signal[[GameObject], None]
    onDestroy: Signal[[], None]
        
    get_cell() -> Cell:
        - returns the cell it's in

    move_to(x: int, y: int):
        - moves to cell at (x, y)
        - fires onMove

    destroy()
        - removes the object from game
        - fires onDestroy
        - disconnects all listeners for onDestroy
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

object_id = 0
class GameObject():
    _destroyed: bool
    def __init__(self, game: GameField, x: int, y: int):
        if type(self) == GameObject:
            raise ValueError("Superclass cannot be instantiated.")
        
        global object_id
        object_id += 1

        self.game = game
        self.id = object_id
        self._cell = game[y, x]
        self._cell.add_object(self)
        self._destroyed = False

        self.onMove = Signal[[int, int], None](game)
        self.onCollision = Signal[[GameObject], None](game)
        self.onTouched = Signal[[GameObject], None](game)
        self.onDestroy = Signal[[], None](game)

        self.game.onObjectAdded.fire(self)

    def __hash__(self):
        return hash(self.id)
    

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

        self.onMove.fire(x, y)

    def destroy(self):
        if self.is_destroyed():
            return
            
        self._cell.remove_object(self)
        self._destroyed = True

        self.onMove.destroy()
        self.onCollision.destroy()
        self.onTouched.destroy()

        self.onDestroy.fire()
        self.onDestroy.destroy()

        del self

    def is_destroyed(self) -> bool:
        return self._destroyed
    
    
    # ---------------------------------
    # internal

    def main_update(self, frame_count: int):
        # if self.is_destroyed():
        #     return
        self.update(frame_count)
    def main_collided_with(self, other: GameObject):
        # if self.is_destroyed():
        #     return
        self.collided_with(other)
        self.onCollision.fire(other)
    def main_touched(self, other: GameObject):
        # if self.is_destroyed():
        #     return
        self.touched(other)
        self.onTouched.fire(other)


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

    
        