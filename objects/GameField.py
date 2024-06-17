from typing import get_args

import pyxel
from pyxelgrid import PyxelGrid

from objects.util import Orientation
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.PlayerController import PlayerController
from objects.Cell import Cell

'''
GameField
    FPS: int
    player: PlayerController
    entities: dict


'''

class GameField(PyxelGrid[Cell]):
    def __init__(self, fps: int, r: int = 15, c: int = 15, dim: int = 8):
        super().__init__(r, c, dim=dim)
        self.FPS = fps
        self.run(title="Battle Tanks Bootleg:tm:", fps=fps)
        

    def init(self) -> None:
        # internals
        pyxel.load("spritesheet.pyxres")
        
        # fill cells
        for r in range(self.r):
            for c in range(self.c):
                Cell(game=self, x=r, y=c)

        # spawn
        self.player = PlayerController(game=self, tank=Tank(game=self, x=0, y=0, team="player"))

    def update(self) -> None:
        # player actions
        self.player.update()
        for r in range(self.r):
            for c in range(self.c):
                cell = self[r, c]
                for obj in cell.get_objects():
                    obj.update()


    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:

        cell = self[i, j]
        for obj in cell.get_objects():
            u = 0
            v = 0
            if isinstance(obj, Tank):
                u_offset = 0 if obj == self.player.tank else self.dim * 4
                u = u_offset + (self.dim * get_args(Orientation).index(obj.orientation))
            elif isinstance(obj, Bullet):
                u_offset = self.dim * 8
                u = u_offset + (self.dim * get_args(Orientation).index(obj.orientation))

            pyxel.bltm(
                x=x,
                y=y,
                w=8,
                h=8,
                tm=0,
                u=u,
                v=v,
                colkey=0
            )
        

    def pre_draw_grid(self) -> None:
        # background
        pyxel.rect(0, 0, self.c*self.dim, self.r*self.dim, 0)