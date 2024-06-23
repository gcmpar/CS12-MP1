from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.GameObject import GameObject
from gamefiles.Signal import Signal

from misc.util import Orientation


'''
A game object that has velocity

Entity:
    orientation: Orientation
    speed: float

    onOrientationChanged: Signal[[Orientation], None]
    onSpeedChanged: Signal[float], None]
    onOutOfBounds = Signal[[], None](game)

    set_orientation(ori: Orientation)
    set_speed(speed: float)

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
    def __init__(self, game: GameField, x: int, y: int,
                 ori: Orientation, speed: float,
                 
                 pre_added: Callable[[GameObject], bool] | None = None,
                 ):
        if type(self) == Entity:
            raise ValueError("Superclass cannot be instantiated.")
        self.orientation = ori
        self.speed = speed
        self.onOrientationChanged = Signal[[Orientation], None](game)
        self.onSpeedChanged = Signal[[float], None](game)
        self.onOutOfBounds = Signal[[], None](game)

        super().__init__(game=game, x=x, y=y, pre_added=pre_added)
        def d():
            self.onOutOfBounds.destroy()
        self.onDestroy.add_listener(d)
    
    def set_orientation(self, ori: Orientation):
        if ori == self.orientation:
            return
        self.orientation = ori
        self.onOrientationChanged.fire(ori)
    def set_speed(self, speed: float):
        if speed == self.speed:
            return
        self.speed = speed
        self.onSpeedChanged.fire(speed)

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