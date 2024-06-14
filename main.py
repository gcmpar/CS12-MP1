import pyxel
from pyxelgrid import PyxelGrid
from PlayerController import PlayerController
from Tank import Tank

def clamp(v, l, h):
    return max(l, min(h, v))

'''
GameField
    player: PlayerController
    tanks: list[Tank]
        - the enemy tanks


'''

class GameField(PyxelGrid[int]):
    def __init__(self, r: int = 5, c: int = 5, dim: int = 5):
        super().__init__(r, c, dim=dim)

    def init(self) -> None:
        # spawn tanks
        self.player = PlayerController(tank=Tank())
        self.tanks = list[Tank]()

        # TEST
        # self.tanks.append(Tank(x=1,y=1))
        # self.tanks.append(Tank(x=2,y=2))
        

    def update(self) -> None:
        # input
        self.player.check_inputs()

        # sanity check
        for tank in [self.player.tank] + self.tanks:
            tank.force_update(
                x = clamp(tank.x, 0, self.c-1),
                y = clamp(tank.y, 0, self.r-1),
            )


    def draw_cell(self, r: int, c: int, x: int, y: int) -> None:

        # draw player tank
        pyxel.load("my_resource.pyxres")
        pyxel.bltm(
            x=self.player.tank.x*self.dim,
            y=self.player.tank.y*self.dim,
            w=self.dim-1,
            h=self.dim-1,
            tm=0,
            u=0,
            v=0,
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
                pyxel.rect(r*self.dim, c*self.dim, self.dim-1, self.dim-1, 5)

    def post_draw_grid(self) -> None:
        ...


game = GameField()
game.run(title="Battle Tanks Bootleg:tm:", fps=60)