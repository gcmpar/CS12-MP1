from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.Cell import Cell

from gamefiles.Signal import Signal
from gamefiles.Modifier import Modifier



'''
Base class for all game objects

GameObject
    game: GameField
    id: int
        - object id
    onMove: Signal[[int, int], None]
    onCollision: Signal[[GameObject], None]
    onTouched: Signal[[GameObject], None]
    onDestroy: Signal[[], None]

    modifiers: list[Modifier]
    onModifierAdded: Signal[[Modifier], None]
    onModifierRemoved: Signal[[Modifier], None]



    _cell: Cell
    _destroyed: bool
        
    get_cell() -> Cell
    move_to(x: int, y: int):
        - moves to cell at (x, y)
        - fires onMove

    destroy()
        - cleanup/deletion function
        - removes the object from game
        - removes all modifiers
        - fires onDestroy
        - disconnects all listeners for onDestroy
    is_destroyed() -> bool

    add_modifier(mod: Modifier)
        - sets modifier and fires onModifierAdded
    remove_modifier(mod: Modifier)
        - removes modifier and fires onModifierRemoved

        
    ---------------------------------
    INTERNALS
        - basically middlemen before the actual overriden method is called

    main_update(frame_count: int)
    main_can_collide(other: GameObject) -> bool
    main_can_touch(other: GameObject) -> bool
    main_collided_with(other: GameObject)
    main_touched(other: GameObject)
    

    ---------------------------------
    INTENDED TO BE OVERRIDEN:

    update(frame_count: int)
        - called every game loop

    i love decoupling
    can_collide(other: GameObject) -> bool = True
        - return True if objects collide with each other (can pass through or not)
        - modified by Modifier with highest priority
    can_touch(other: GameObject) -> bool = True
        - return True if objects can touch each other (when same cell)
        - modified by Modifier with highest priority

    collided_with(other: GameObject)
        - called whenever a GameObject collides with another
        - called on both for each other
        - called along with onCollision

    touched(other: GameObject)
        - called whenever a GameObject is on the same cell as another
        - called on both for each other
        - called along with onTouched
'''

object_id = 0
class GameObject():
    modifiers: list[Modifier]
    _destroyed: bool
    def __init__(self, game: GameField, x: int, y: int):
        if type(self) == GameObject:
            raise ValueError("Superclass cannot be instantiated.")
        
        global object_id
        object_id += 1

        self.game = game
        self.id = object_id
        self.onMove = Signal[[int, int], None](game)
        self.onCollision = Signal[[GameObject], None](game)
        self.onTouched = Signal[[GameObject], None](game)
        self.onDestroy = Signal[[], None](game)

        self.modifiers = []
        self.onModifierAdded = Signal[[Modifier], None](game)
        self.onModifierRemoved = Signal[[Modifier], None](game)


        self._cell = game[y, x]
        self._cell.add_object(self)
        self._destroyed = False
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

        [self.remove_modifier(mod) for mod in self.modifiers]

        self.onDestroy.fire()
        self.onDestroy.destroy()

        del self

    def is_destroyed(self) -> bool:
        return self._destroyed
    

    def add_modifier(self, mod: Modifier):
        if mod in self.modifiers:
            return
        self.modifiers.append(mod)
        self.modifiers.sort(key=lambda e: e.priority)
        mod.init(mod)
        self.onModifierAdded.fire(mod)

    def remove_modifier(self, mod: Modifier):
        if mod not in self.modifiers:
            return
        self.modifiers.remove(mod)
        self.modifiers.sort(key=lambda e: e.priority)
        mod.destroy(mod)
        self.onModifierRemoved.fire(mod)
    
    
    # ---------------------------------
    # internal

    def main_update(self, frame_count: int):
        # if self.is_destroyed():
        #     return
        self.update(frame_count)
        for mod in self.modifiers:
            mod.update(mod, frame_count)

    def main_can_collide(self, other: GameObject) -> bool:
        if len(self.modifiers) != 0:
            mod = self.modifiers[-1]
            b = mod.can_collide(mod, other)
            if b is not None:
                return b
        return self.can_collide(other)

    def main_can_touch(self, other: GameObject) -> bool:
        if len(self.modifiers) != 0:
            mod = self.modifiers[-1]
            b = mod.can_touch(mod, other)
            if b is not None:
                return b
        return self.can_touch(other)
    
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
    
    def can_touch(self, other: GameObject) -> bool:
        return True
    
    def collided_with(self, other: GameObject):
        pass
    def touched(self, other: GameObject):
        pass

    
        