from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Orientation
    from objects.Tank import Tank

from objects.GameObject import GameObject
from objects.Entity import Entity
from objects.Mirror import Mirror

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
    _last_mirror_hit: Mirror | None
    def __init__(self, game: GameField, x: int, y: int, owner: Tank, ori: Orientation, speed: int=15):
        super().__init__(game=game, x=x, y=y, ori=ori, speed=speed)
        self._last_mirror_hit = None

        self.owner = owner

        def on_move():
            cell = self.get_cell()
            if self._last_mirror_hit is not None:
                if self._last_mirror_hit not in cell.get_objects():
                    self._last_mirror_hit = None

        self.bind_to_move(on_move)

    def can_collide(self, other: GameObject):
        if isinstance(other, Mirror):
            return False
        
        return True

    def collided_with(self, other: GameObject):
        self.destroy()
    
    def touched(self, other: GameObject):
        if isinstance(other, Mirror) and self._last_mirror_hit != other: # debounce
            self._last_mirror_hit = other

            ref_ori = other.reflect_orientation
            
            c = ref_map[self.orientation]
            c = (c[1], c[0])
            if ref_ori == "northeast":
                c = (-c[0], -c[1])

            new_ori = ref_map_inv[c]
            self.orientation = new_ori
    
    def out_of_bounds(self):
        self.destroy()
