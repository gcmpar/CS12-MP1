from typing import get_args

import pyxel
from pyxelgrid import PyxelGrid
from objects.Tank import Tank
from objects.util import Direction

controls = {
    "east": pyxel.KEY_D,
    "north": pyxel.KEY_W,
    "west": pyxel.KEY_A,
    "south": pyxel.KEY_S,
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
        for dir in get_args(Direction):
            if pyxel.btn(controls[dir]):
                self.tank.move(dir)
                break