from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Orientation, Team

from objects.Entity import Entity
from objects.GameObject import GameObject
from objects.Bullet import Bullet

'''
Tank
    team: Team
    isMoving: bool
    stats: {
        "health": float
        "movementSpeed: float
        "fireRate: int
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
    isMoving: bool
    _bulletFired: bool
    _canFireBullet: bool
    def __init__(self, game: GameField, x: int, y: int, team: Team,
                 
                 health: float,
                 movement_speed: float,
                 fire_rate: float
                
                ):
        
        super().__init__(game, x, y, ori="north", speed=0)
        self.team = team
        self.isMoving = False

        self.stats = {
            "health": health,
            "movementSpeed": movement_speed,
            "fireRate": fire_rate,
        }

        self._lastFireFrame = 0
        self._bulletFired = False
        self._canFireBullet = True
    
    def turn(self, ori: Orientation):
        self.orientation = ori
    def start_moving(self):
        self.speed = self.stats["movementSpeed"]
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
        self._bulletFired = True

        bullet = Bullet(
            game=self.game,
            x=self.get_cell().x + x_move,
            y=self.get_cell().y + y_move,
            owner=self,
            ori=ori,
            speed=15
            )
        return bullet
    
    def can_fire_bullet(self) -> bool:
        return self._canFireBullet

    
    def update(self, frame_count: int):
        if self.stats["health"] <= 0:
            self.destroy()
            return
        if self._bulletFired:
            self._bulletFired = False
            self._lastFireFrame = frame_count
        self._canFireBullet = not (frame_count < (self._lastFireFrame + (self.game.FPS / self.stats["fireRate"])))

    def can_collide(self, other: GameObject):
        if isinstance(other, Bullet):
            if self.team == "enemy" and other.owner.team == "enemy":
                return False
                
        return True

    def collided_with(self, other: GameObject):
        if isinstance(other, Bullet):
            self.stats["health"] -= 1
                    
        