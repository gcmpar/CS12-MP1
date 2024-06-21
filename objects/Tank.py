from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Orientation, Team

from objects.Entity import Entity
from objects.GameObject import GameObject
from objects.Bullet import Bullet

from misc.Signal import Signal
from misc.Stat import Stat

'''
Tank
    type: str
        - descriptor for rendering or other managers
    team: Team
    isMoving: bool
    onBulletFired: Signal[[Bullet], None]
    stats: {
        "health": Stat
        "movementSpeed: Stat
        "fireRate: Stat
    }

    turn(ori: Orientation)
    start_moving()
    stop_moving()
        
    
    fire_bullet() --> Bullet | None
        - fires bullet
        - returns the bullet if successful
        - fires onBulletFired
    
    can_fire_bullet() -> bool
        - based on fireRate

'''

class Tank(Entity):
    team: Team
    isMoving: bool
    _bulletFired: bool
    _canFireBullet: bool
    def __init__(self, game: GameField, x: int, y: int, team: Team, tank_type: str,
                 
                 health: float,
                 movement_speed: float,
                 fire_rate: float
                
                ):
        self.team = team
        self.type = tank_type
        self.isMoving = False
        self.onBulletFired = Signal[[Bullet], None](game)

        self.stats = {
            "health": Stat(health),
            "movementSpeed": Stat(movement_speed),
            "fireRate": Stat(fire_rate),
        }



        self._lastFireFrame = 0
        self._bulletFired = False
        self._canFireBullet = True

        super().__init__(game, x, y, ori="north", speed=0)
        def d():
            self.onBulletFired.destroy()
        self.onDestroy.add_listener(d)



    
    def turn(self, ori: Orientation):
        self.orientation = ori
    def start_moving(self):
        self.speed = self.stats["movementSpeed"].current
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
        self.onBulletFired.fire(bullet)
        return bullet
    
    def can_fire_bullet(self) -> bool:
        return self._canFireBullet

    
    def update(self, frame_count: int):
        if self.stats["health"].current <= 0:
            self.destroy()
            return
        if self._bulletFired:
            self._bulletFired = False
            self._lastFireFrame = frame_count

        if self.stats["fireRate"].current != 0: # sneaky
            self._canFireBullet = not (frame_count < (self._lastFireFrame + (self.game.FPS / self.stats["fireRate"].current)))

    def can_touch(self, other: GameObject):
        if isinstance(other, Bullet):
            if self.team == "enemy" and other.owner.team == "enemy":
                return False
                
        return True

    def touched(self, other: GameObject):
        if isinstance(other, Bullet):
            self.stats["health"].current -= 1
                    
        