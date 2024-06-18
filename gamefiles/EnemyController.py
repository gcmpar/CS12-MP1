from __future__ import annotations
from typing import TYPE_CHECKING, get_args

import pyxel
import random

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

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

class EnemyController():
    _movement_last_ori: Orientation
    def __init__(self, game: GameField, tank: Tank):
        self.game = game
        self.tank = tank


        self.fireInterval = random.randint(60,120)
        self.lastFireTime = 0

        self.moveInterval = random.randint(60,120)
        self.lastMoveTime = 0

        self._movement_held: dict[str, int] = {}
        for c in get_args(Orientation):
            self._movement_held[c] = 0
        self._movement_last_ori = self.tank.ori
    
    def update(self, frame_count: int):
        # for c, btn in controls.items():
        #     if pyxel.btn(btn):
        #         self._movement_held[c] += 1
        #     else:
        #         self._movement_held[c] = 0

        if frame_count - self.lastMoveTime > self.moveInterval:

            randomMove = random.choice(get_args(Orientation))
            self._movement_held[randomMove] += 1
            
            
            # print(self._movement_held)

            # movement (whatever was pressed last)
            moved = False
            orientations = get_args(Orientation)
            least_held: int | None = None
            ori_priority = orientations[0]

            for ori in get_args(Orientation):
                if self._movement_held[ori] == 0:
                    continue

                if least_held is None or self._movement_held[ori] < least_held:
                    moved = True
                    least_held = self._movement_held[ori]
                    ori_priority = ori

            if not moved:
                self.tank.speed = 0
                ori_priority = self._movement_last_ori
            else:
                self.tank.speed = 5
                self._movement_last_ori = ori_priority
            
            self.tank.orientation = ori_priority
            
            for move in get_args(Orientation):
                self._movement_held[move] = 0

            self.lastMoveTime = frame_count
            self.moveInterval = random.randint(60,120)
        
        # fire
        if frame_count - self.lastFireTime > self.fireInterval:
            self.tank.fire()
            self.lastFireTime = frame_count
            self.fireInterval = random.randint(60,120)
            