from __future__ import annotations
from typing import TYPE_CHECKING, get_args

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.Bullet import Bullet

from objects.Tank import Tank
from misc.util import Orientation

from resources.controls import CONTROLS

'''
input checker for player

PlayerController:
    tank: Tank
        - the tank the player controls
    
    update(frame_count: int)
        - used by the main GameField to check input presses every frame and control tank accordingly
        - for movement, prioritize the key that was last held
        - for firing bullets, only fire bullet if the last bullet doesn't exist/was already destroyed

'''

class PlayerController():
    _movementLastOri: Orientation
    _bullet: Bullet | None
    def __init__(self, game: GameField, tank: Tank):
        self.game = game
        self.tank = tank

        self._movementHeld: dict[str, int] = {}
        for c in CONTROLS.keys():
            self._movementHeld[c] = 0
        self._movementLastOri = "north"

        self._bullet = None

        def record_bullet(bullet: Bullet):
            self._bullet = bullet
            def unrecord_bullet():
                self._bullet = None
            bullet.onDestroy.add_listener(unrecord_bullet)
        self.tank.onBulletFired.add_listener(record_bullet)
    
    def update(self, frame_count: int):
        for c, data in CONTROLS.items():
            if pyxel.btn(data["btn"]):
                self._movementHeld[c] += 1
            else:
                self._movementHeld[c] = 0

        # movement (whatever was pressed last)
        move = False
        orientations = get_args(Orientation)
        least_held: int | None = None
        ori_priority = orientations[0]

        for ori in get_args(Orientation):
            if self._movementHeld[ori] == 0:
                continue

            if least_held is None or self._movementHeld[ori] < least_held:
                move = True
                least_held = self._movementHeld[ori]
                ori_priority = ori

        if not move:
            self.tank.stop_moving()
            ori_priority = self._movementLastOri
        else:
            self.tank.start_moving()
            self._movementLastOri = ori_priority
        
        self.tank.set_orientation(ori_priority)
        
        # fire
        if pyxel.btn(CONTROLS["fire"]["btn"]):
            allow = self._bullet is None
            for mod in self.tank.get_modifiers():
                if mod.type == "TimeStopBuff":
                    allow = True
            if allow:
                self._bullet = self.tank.fire_bullet()
            