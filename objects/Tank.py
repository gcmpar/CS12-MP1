from __future__ import annotations
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Orientation, Team

from objects.Entity import Entity
from objects.GameObject import GameObject
from objects.Bullet import Bullet

'''
Tank
    orientation: Orientation
    speed: int


    team: Team
    fire_rate: int
        - how many bullets the tank can fire per second
    
    fire()
        - fires bullet

'''

class Tank(Entity):
    orientation: Orientation
    def __init__(self, game: GameField, x: int, y: int, ori: Orientation = "east", team: Team = "enemy"):
        super().__init__(game, x, y, ori=ori)
        self.team = team
        self.fire_rate = 1


        self._last_fire_frame = 0
        self._bullet_iframes = dict[Bullet, int]()
    
    def fire(self):
        if self.is_destroyed():
            return

        cell = self.get_cell()
        ori = self.orientation
        x_move = 1 if ori == "east" else -1 if ori == "west" else 0
        y_move = 1 if ori == "south" else -1 if ori == "north" else 0
        bullet_x = cell.x + x_move
        bullet_y = cell.y + y_move

        if not self.game.in_bounds(bullet_y, bullet_x):
            return

        # fire cap
        if pyxel.frame_count < (self._last_fire_frame + (self.game.FPS / self.fire_rate)):
            return
        self._last_fire_frame = pyxel.frame_count

        bullet = Bullet(
            game=self.game,
            x=self.get_cell().x + x_move,
            y=self.get_cell().y + y_move,
            owner=self,
            ori=ori,
            speed=15
            )
        self._bullet_iframes[bullet] = 0
    
    def update(self, frame_count: int):
        for bullet in self._bullet_iframes.copy().keys():
            if self._bullet_iframes[bullet] > 2:
                del self._bullet_iframes[bullet]

    def can_collide(self, other: GameObject):
        if isinstance(other, Bullet):
            if other in self._bullet_iframes:
                return False
            if self.team == "enemy" and other.owner.team == "enemy":
                return False
                
        return True

    def collided_with(self, other: GameObject):
        if isinstance(other, Bullet):
                self.destroy()
                    
        