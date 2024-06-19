from __future__ import annotations
from typing import TYPE_CHECKING, get_args, Callable

import random, math

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.Tank import Tank
from misc.util import Orientation

'''
EnemyController:
    tank: Tank
    update()

'''

def random_interval(fps: int):
    return random.randint(math.floor(fps/4), math.floor(fps/1.5))

class EnemyController():
    _moveOnce: Callable[[], None] | None
    def __init__(self, game: GameField, tank: Tank):
        self.game = game
        self.tank = tank


        self._rotateInterval = random_interval(game.FPS)
        self._lastRotateTime = 0

        self._moveInterval = random_interval(game.FPS)
        self._lastMoveTime = 0
        self._moveOnce = None

        self._fireInterval = random_interval(game.FPS)
        self._lastFireTime = 0

    def update(self, frame_count: int):

        # rotate
        if frame_count - self._lastRotateTime > self._rotateInterval:
            self._lastRotateTime = frame_count
            self._rotateInterval = random_interval(self.game.FPS)

            self.tank.turn(random.choice(get_args(Orientation)))

        # move
        if frame_count - self._lastMoveTime > self._moveInterval:
            self._lastMoveTime = frame_count
            self._moveInterval = random_interval(self.game.FPS)

            # just makes sure it moves one cell only each time
            if self._moveOnce is not None:
                self.tank.on_move.remove_listener(self._moveOnce)
            self.tank.start_moving()

            def moveOnce():
                self.tank.stop_moving()
                self.tank.on_move.remove_listener(moveOnce)
                self._moveOnce = None
            self.tank.on_move.add_listener(moveOnce)
            self._moveOnce = moveOnce
        
        # fire
        if frame_count - self._lastFireTime > self._fireInterval:
            self._lastFireTime = frame_count
            self._fireInterval = random_interval(self.game.FPS)

            self.tank.fire_bullet()
            