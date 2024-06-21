from __future__ import annotations
from typing import TYPE_CHECKING, get_args, Callable

import random

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.Bullet import Bullet

from objects.Tank import Tank
from misc.util import Orientation




'''
AI for enemy tanks

EnemyController:
    tank: Tank
    update(frame_count: int)
        - called every game loop

'''

def random_interval() -> float:
    return random.random() * 2

class EnemyController():
    _moveOnce: Callable[[int, int], None] | None
    def __init__(self, game: GameField, tank: Tank):
        self.game = game
        self.tank = tank


        self._rotateInterval = random_interval()
        self._lastRotateTime = 0

        self._moveInterval = random_interval()
        self._lastMoveTime = 0
        self._moveCount = 0

        self._fireInterval = random_interval()
        self._lastFireTime = 0
        self._fireCount = 0

    def update(self, frame_count: int):

        # rotate
        if frame_count > self._lastRotateTime + (self.game.FPS * self._rotateInterval):
            self._lastRotateTime = frame_count
            self._rotateInterval = random_interval()

            self.tank.turn(random.choice(get_args(Orientation)))

        # move
        if self._moveCount <= 0 and frame_count > self._lastMoveTime + (self.game.FPS * self._moveInterval):
            self._lastMoveTime = frame_count
            self._moveCount = random.randint(1, 5)
            self.tank.start_moving()

            def moveOnce(x: int, y: int):

                self._moveCount -= 1

                if self._moveCount <= 0:
                    self._lastMoveTime = frame_count
                    self._moveInterval = random_interval()
                    self.tank.stop_moving()
                    self.tank.onMove.remove_listener(moveOnce)
                    
            self.tank.onMove.add_listener(moveOnce)
        
        # fire
        if self._fireCount > 0:
            self.tank.fire_bullet()
        elif frame_count > self._lastFireTime + (self.game.FPS * self._fireInterval):
            self._fireCount = random.randint(1, 5)

            def fireOnce(bullet: Bullet):

                self._fireCount -= 1

                if self._fireCount <= 0:
                    self._lastFireTime = frame_count
                    self._fireInterval = random_interval()

            self.tank.onBulletFired.add_listener(fireOnce)
            