from typing import get_args

import pyxel
from pyxelgrid import PyxelGrid

from objects.util import Direction
from objects.Tank import Tank
from objects.PlayerController import PlayerController

'''
GameField
    player: PlayerController
    tanks: list[Tank]
        - the enemy tanks


'''

FPS = 60

class GameField(PyxelGrid[int]):
    def __init__(self, r: int = 15, c: int = 15, dim: int = 9):
        super().__init__(r, c, dim=dim)

    def init(self) -> None:
        # internals
        self.FPS = FPS
        pyxel.load("sprites/tank_player.pyxres")
        
        # spawn tanks
        self.player = PlayerController(game=self, tank=Tank(game=self))
        self.tanks = list[Tank]()

        # TEST
        # self.tanks.append(Tank(x=1,y=1))
        # self.tanks.append(Tank(x=2,y=2))
        

    def update(self) -> None:
        # player actions
        self.player.update()


    def draw_cell(self, r: int, c: int, x: int, y: int) -> None:

        # draw player tank
        pyxel.bltm(
            x=self.player.tank.x*self.dim,
            y=self.player.tank.y*self.dim,
            w=8,
            h=8,
            tm=0,
            u=8 * get_args(Direction).index(self.player.tank.direction),
            v=0,
            colkey=0
        )
        #pyxel.rect(self.player.tank.x*self.dim, , self.dim-1, self.dim-1, 254)

        # draw other tanks
        for tank in self.tanks:
            pyxel.rect(tank.x*self.dim, tank.y*self.dim, self.dim-1, self.dim-1, 128)

    def pre_draw_grid(self) -> None:
        # background
        pyxel.rect(0, 0, self.c*self.dim, self.r*self.dim, 0)

        for r in range(self.r):
            for c in range(self.c):
                pyxel.rectb(r*self.dim, c*self.dim, self.dim-1, self.dim-1, 1)

    def post_draw_grid(self) -> None:
        ...


game = GameField()
game.run(title="Battle Tanks Bootleg:tm:", fps=FPS)