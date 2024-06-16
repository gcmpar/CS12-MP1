from typing import get_args

import pyxel
from pyxelgrid import PyxelGrid
from objects.Tank import Tank
from objects.util import Orientation

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
    from objects.Cell import Cell

    def __init__(self, game: PyxelGrid[Cell], tank: Tank):
        self._game = game

        self.tank = tank
    
    def update(self):
        # movement
        for ori in get_args(Orientation):
            if pyxel.btn(controls[ori]):
                self.tank.move(ori)
                break
        
        if pyxel.btn(controls["fire"]):
            self.tank.fire()