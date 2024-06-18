
import pyxel
from pyxelgrid import PyxelGrid
from gamefiles.Cell import Cell
from gamefiles.PlayerController import PlayerController
from gamefiles.PhysicsManager import PhysicsManager
from gamefiles.Renderer import Renderer


from objects.Tank import Tank
from objects.Brick import Brick
from objects.Stone import Stone
from objects.Mirror import Mirror

'''
GameField
    FPS: int
    physics: PhysicsManager
    renderer: Renderer
    
    player: PlayerController


'''

class GameField(PyxelGrid[Cell]):
    def __init__(self, fps: int, r: int = 25, c: int = 15, dim: int = 8):
        super().__init__(r, c, dim=dim)
        self.FPS = fps
        self.run(title="Battle Tanks Bootleg:tm:", fps=fps)
        

    def init(self) -> None:
        # internals
        self.physics = PhysicsManager(self)
        self.renderer = Renderer(self)
        pyxel.load("resources/spritesheet.pyxres")
        
        # fill cells
        for r in range(self.r):
            for c in range(self.c):
                Cell(game=self, x=c, y=r)

        # spawn
        self.player = PlayerController(game=self, tank=Tank(game=self, x=0, y=0, team="player"))
        Brick(game=self, x=2,y=2)
        Stone(game=self, x=1,y=1)
        Mirror(game=self, x=8, y=10, ref_ori="northeast")
        Mirror(game=self, x=12, y=12, ref_ori="southeast")

    def update(self) -> None:
        # TODO 0 game state

        # 1 input handling
        self.player.update(pyxel.frame_count)

        # 2 physics
        self.physics.update(pyxel.frame_count)

        # 3 game objects
        [obj.main_update(pyxel.frame_count) for r in range(self.r) for c in range(self.c) for obj in self[r, c].get_objects()]

        # TODO 3 enemy

    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        self.renderer.update_cell(pyxel.frame_count, i, j, x, y)

    def pre_draw_grid(self) -> None:
        # background
        pyxel.rect(0, 0, self.c*self.dim, self.r*self.dim, 0)