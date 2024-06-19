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
    team: Team
    is_moving: bool
    stats: {
        "health": float
        "movement_speed": float
        "fire_rate": int
    }

    turn(ori: Orientation)
    start_moving()
    stop_moving()
        
    
    fire_bullet() --> Bullet | None
        - fires bullet
        - returns the bullet if successful
    
    can_fire_bullet() -> bool

'''

class Tank(Entity):
    team: Team
    is_moving: bool
    def __init__(self, game: GameField, x: int, y: int, team: Team,
                 
                 health: float,
                 movement_speed: float,
                 fire_rate: float
                
                ):
        
        super().__init__(game, x, y, ori="east", speed=0)
        self.team = team
        self.is_moving = False

        self.stats = {
            "health": health,
            "movement_speed": movement_speed,
            "fire_rate": fire_rate,
        }

        self._last_fire_frame = 0
        self._bullet_iframes = dict[Bullet, int]()
    
    def turn(self, ori: Orientation):
        self.orientation = ori
    def start_moving(self):
        self.speed = self.stats["movement_speed"]
    def stop_moving(self):
        self.speed = 0

    def fire_bullet(self) -> Bullet | None:
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
        if not self.can_fire_bullet():
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

        def cancel_iframes():
            del self._bullet_iframes[bullet]
            bullet.on_move.remove_listener(cancel_iframes)
        bullet.on_move.add_listener(cancel_iframes)

        return bullet
    
    def can_fire_bullet(self) -> bool:
        if pyxel.frame_count < (self._last_fire_frame + (self.game.FPS / self.stats["fire_rate"])):
            return False
        return True

    
    def update(self, frame_count: int):
        if self.stats["health"] <= 0:
            self.destroy()
            return
        
        for bullet in list(self._bullet_iframes):
            if self._bullet_iframes[bullet] > self.game.FPS/10:
                del self._bullet_iframes[bullet]
                continue
            self._bullet_iframes[bullet] += 1

    def can_collide(self, other: GameObject):
        if isinstance(other, Bullet):
            if self.team == "enemy" and other.owner.team == "enemy":
                return False
                
        return True

    def collided_with(self, other: GameObject):
        if isinstance(other, Bullet):
            if other in self._bullet_iframes:
                return
            self.stats["health"] -= 1
                    
        