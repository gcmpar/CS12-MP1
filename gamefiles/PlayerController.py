from __future__ import annotations
from typing import TYPE_CHECKING, get_args

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.Bullet import Bullet

from objects.Tank import Tank
from misc.util import Orientation


controls = {
    "east": pyxel.KEY_D,
    "north": pyxel.KEY_W,
    "west": pyxel.KEY_A,
    "south": pyxel.KEY_S,
    "fire": pyxel.KEY_SPACE,
}
'''
PlayerController:
    tank: Tank
        - the tank the player controls
    
    update()
        - used by the main GameField to check input presses every frame and control tank accordingly

'''

class PlayerController():
    _movement_last_ori: Orientation
    _bullet: Bullet | None
    def __init__(self, game: GameField, tank: Tank):
        self.game = game
        self.tank = tank

        self._movement_held: dict[str, int] = {}
        for c in get_args(Orientation):
            self._movement_held[c] = 0
        self._movement_last_ori = "north"

        self._bullet = None
    
    def update(self, frame_count: int):
        for c, btn in controls.items():
            if pyxel.btn(btn):
                self._movement_held[c] += 1
            else:
                self._movement_held[c] = 0

        # movement (whatever was pressed last)
        move = False
        orientations = get_args(Orientation)
        least_held: int | None = None
        ori_priority = orientations[0]

        for ori in get_args(Orientation):
            if self._movement_held[ori] == 0:
                continue

            if least_held is None or self._movement_held[ori] < least_held:
                move = True
                least_held = self._movement_held[ori]
                ori_priority = ori

        if not move:
            self.tank.stop_moving()
            ori_priority = self._movement_last_ori
        else:
            self.tank.start_moving()
            self._movement_last_ori = ori_priority
        
        self.tank.turn(ori_priority)
        
        # fire
        if pyxel.btn(controls["fire"]):
            if self._bullet is not None and self._bullet.is_destroyed():
                self._bullet = None
            if self._bullet is None:
                self._bullet = self.tank.fire_bullet()
            