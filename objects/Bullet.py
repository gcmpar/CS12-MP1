from __future__ import annotations
from typing import TYPE_CHECKING

import pyxel
from pyxelgrid import PyxelGrid

from objects.Cell import Cell
from objects.GameObject import GameObject

if TYPE_CHECKING:
    from objects.Tank import Tank


from objects.util import Orientation

'''
Bullet:
    owner: Tank
        - tank who fired the bullet

    orientation: Orientation
        - where bullet is currently facing
    
    speed: int
        - how many cells the bullet can move per second
'''

class Bullet(GameObject):
    def __init__(self, game: PyxelGrid[Cell], x: int, y: int, owner: Tank, ori: Orientation, speed: int=15):
        super().__init__(game, x, y)
        self._last_move_frame = 0

        self.owner = owner
        self.orientation = ori
        self.speed = speed
        
    
    def update(self):
        # movement cap
        if pyxel.frame_count < (self._last_move_frame + (self._game.FPS / self.speed)):
            return False
        self._last_move_frame = pyxel.frame_count

        ori = self.orientation
        x_move = 1 if ori == "east" else -1 if ori == "west" else 0
        y_move = 1 if ori == "south" else -1 if ori == "north" else 0

        self.move_to(self.get_cell().x + x_move, self.get_cell().y + y_move)
    
    def can_collide(self, other: GameObject):
        if self.owner.team == "enemy":
            if isinstance(other, Tank) and other.team == "enemy":
                return False
        
        return True

    def collided_with(self, other: GameObject):
        self.delete()
    
    def out_of_bounds(self):
        self.delete()
