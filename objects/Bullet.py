from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.Tank import Tank

from misc.util import Orientation, ReflectOrientation, orientation_to_ref_vector, flip_orientation

from objects.GameObject import GameObject
from objects.Entity import Entity
from objects.Mirror import Mirror
from objects.Water import Water
from objects.Karma import Karma

'''
Bullet:
    orientation: Orientation
    speed: float


    owner: Tank
        - tag for tank who fired the bullet
        - can be changed
'''


class Bullet(Entity):
    owner: Tank | None
    _lastMirrorHit: Mirror | None
    _lastKarmaHit: Karma | None
    def __init__(self, game: GameField, x: int, y: int,
                 ori: Orientation, speed: float,
                 owner: Tank | None = None,
                 pre_added: Callable[[GameObject], bool] | None = None
                 ):
        self.owner = owner

        self._lastMirrorHit = None
        self._lastKarmaHit = None

        super().__init__(game=game, x=x, y=y, pre_added=pre_added, ori=ori, speed=speed)
        def on_move(x: int, y: int):
            cell = self.get_cell()
            if self._lastMirrorHit is not None:
                if self._lastMirrorHit not in cell.get_objects():
                    self._lastMirrorHit = None
            if self._lastKarmaHit is not None:
                if self._lastKarmaHit not in cell.get_objects():
                    self._lastKarmaHit = None

        self.onMove.add_listener(on_move)

    def can_collide(self, other: GameObject):
        return False
    
    def touched(self, other: GameObject):
        if isinstance(other, Mirror):
            if self._lastMirrorHit != other: # debounce
                self._lastMirrorHit = other

                ori = self.orientation
                ref_ori: ReflectOrientation = other.reflectOrientation
                new_ori = orientation_to_ref_vector(ori, ref_ori)

                self.set_orientation(new_ori)
        elif isinstance(other, Karma):
            if self._lastKarmaHit != other: # debounce
                self._lastKarmaHit = other
                self.set_orientation(flip_orientation(self.orientation))
        elif not isinstance(other, Water):
            self.destroy()
    
    def out_of_bounds(self):
        self.destroy()
        