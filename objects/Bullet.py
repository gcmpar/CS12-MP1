from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Orientation
    from objects.Tank import Tank
    
from objects.GameObject import GameObject
from objects.Entity import Entity
from objects.Mirror import Mirror
from objects.Water import Water

'''
Bullet:
    orientation: Orientation
    speed: int


    owner: Tank
        - tank who fired the bullet
'''

# maps Orientation to vector
ref_map: dict[Orientation, tuple[int, int]] = {
                "east": (1, 0),
                "north": (0, -1),
                "west": (-1, 0),
                "south": (0, 1)
}
# maps vector to Orientation (inverse of above)
ref_map_inv: dict[tuple[int, int], Orientation] = {v: k for k, v in ref_map.items()}


class Bullet(Entity):
    orientation: Orientation
    _lastMirrorHit: Mirror | None
    def __init__(self, game: GameField, x: int, y: int, owner: Tank, ori: Orientation, speed: int=15):
        self._lastMirrorHit = None
        self.owner = owner

        super().__init__(game=game, x=x, y=y, ori=ori, speed=speed)
        def on_move(x: int, y: int):
            cell = self.get_cell()
            if self._lastMirrorHit is not None:
                if self._lastMirrorHit not in cell.get_objects():
                    self._lastMirrorHit = None

        self.onMove.add_listener(on_move)

    def can_collide(self, other: GameObject):
        return False
    
    def touched(self, other: GameObject):
        if isinstance(other, Mirror):
            if self._lastMirrorHit != other: # debounce
                self._lastMirrorHit = other

                ref_ori = other.reflectOrientation
                
                c = ref_map[self.orientation]
                c = (c[1], c[0])
                if ref_ori == "northeast":
                    c = (-c[0], -c[1])

                new_ori = ref_map_inv[c]
                self.orientation = new_ori
        elif not isinstance(other, Water):
            self.destroy()
    
    def out_of_bounds(self):
        self.destroy()
        