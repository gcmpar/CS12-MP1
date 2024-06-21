from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Orientation

from objects.GameObject import GameObject
from gamefiles.Signal import Signal


'''
A game object that has velocity

Entity:
    orientation: Orientation
    speed: int

    onOutOfBounds = Signal[[], None](game)

    ---------------------------------
    INTERNALS
        - basically middlemen before the actual overriden method is called

    main_out_of_bounds()
    

    ---------------------------------
    INTENDED TO BE OVERRIDEN:
    
    out_of_bounds()
        - called whenever the object attempted to move out of bounds
        - called along with onOutOfBounds

'''
class Entity(GameObject):
    orientation: Orientation
    def __init__(self, game: GameField, x: int, y: int, ori: Orientation, speed: int = 0):
        if type(self) == Entity:
            raise ValueError("Superclass cannot be instantiated.")
        self.orientation = ori
        self.speed = speed
        self.onOutOfBounds = Signal[[], None](game)

        super().__init__(game, x, y)
        def d():
            self.onOutOfBounds.destroy()
        self.onDestroy.add_listener(d)

    # ---------------------------------
    # internal
    def main_out_of_bounds(self):
        if self.is_destroyed():
            return
        self.out_of_bounds()
        self.onOutOfBounds.fire()

    # ---------------------------------
    # method overrides
    def out_of_bounds(self):
        pass