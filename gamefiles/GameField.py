
import pyxel
import enum

from pyxelgrid import PyxelGrid
from gamefiles.Cell import Cell
from gamefiles.PlayerController import PlayerController
from gamefiles.EnemyController import EnemyController
from gamefiles.PhysicsManager import PhysicsManager
from gamefiles.Renderer import Renderer

from resources.StageFile import Stage

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

class GameState(enum.Enum):
    READY = 0
    ONGOING = 1
    WIN = 2
    LOSE = 3


class GameField(PyxelGrid[Cell]):
    def __init__(self, fps: int, r: int = 15, c: int = 15, dim: int = 8):
        super().__init__(r, c, dim=dim)
        self.FPS = fps
        self.run(title="Battle Tanks Bootleg:tm:", fps=fps)
        

    def init(self) -> None:
        # internals
        self.physics = PhysicsManager(self)
        self.renderer = Renderer(self)
        pyxel.load("resources/spritesheet.pyxres")

        # self.StageFile = Stage(game=self)
        # self.currStage = self.StageFile.stage1
        # self.StageFile.generate_stage(self.currStage)
        # print(type((self.StageFile.stage1)))
        
        # fill cells
        for r in range(self.r):
            for c in range(self.c):
                Cell(game=self, x=c, y=r)

        # spawn player
        # self.player = self.StageFile.player
        self.player = PlayerController(
            game=self,
            tank=Tank(game=self, x=0, y=0, team="player",
                      
                      health=1,
                      movement_speed=5,
                      fire_rate=1,
                )
            )
        Brick(game=self, x=2,y=2)
        Stone(game=self, x=1,y=1)
        Mirror(game=self, x=2, y=4, ref_ori="northeast")
        Mirror(game=self, x=2, y=6, ref_ori="northeast")
        Mirror(game=self, x=12, y=6, ref_ori="southeast")
        Mirror(game=self, x=12, y=4, ref_ori="southeast")

        # spawn enemies
        self.enemies = list[EnemyController]()
        enemy1 = EnemyController(
            game=self,
            tank=Tank(game=self, x=6, y=9, team="player",
                      
                      health=1,
                      movement_speed=5,
                      fire_rate=1,
                )
            )
        enemy2 = EnemyController(
            game=self,
            tank=Tank(game=self, x=9, y=6, team="player",
                      
                      health=1,
                      movement_speed=5,
                      fire_rate=1,
                )
            )
        self.enemies.append(enemy1)
        self.enemies.append(enemy2)

        self.currentGameState = GameState.READY


    def update(self) -> None:
        # TODO 0 game state
        # if not self.enemies:
        #     # print("Win")
        #     return
        # if self.player.tank.is_destroyed():
        #     # print("Lose")
        #     return
        if self.currentGameState == GameState.READY:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.currentGameState = GameState.ONGOING
            else:
                return

        if self.currentGameState == GameState.ONGOING:
            # 1 input handling
            self.player.update(pyxel.frame_count)

            # 2 physics
            self.physics.update(pyxel.frame_count)

            # 3 game objects
            [obj.main_update(pyxel.frame_count) for r in range(self.r) for c in range(self.c) for obj in self[c, r].get_objects()]

            # TODO 4 enemy
            for enemy in self.enemies:
                enemy.update(pyxel.frame_count)
                if enemy.tank.is_destroyed():
                    self.enemies.remove(enemy)
            
            if not self.enemies:
                self.currentGameState = GameState.WIN

            if self.player.tank.is_destroyed():
                self.currentGameState = GameState.LOSE

        
        
        


    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        self.renderer.update_cell(pyxel.frame_count, i, j, x, y)

    def pre_draw_grid(self) -> None:
        # background
        pyxel.rect(0, 0, self.c*self.dim, self.r*self.dim, 0)

    def post_draw_grid(self) -> None:
        if self.currentGameState == GameState.WIN:
            # pyxel.text(pyxel.width//2, pyxel.height//2, "YOU WIN", 12)
            pyxel.text((pyxel.width - (len("VICTORY") * pyxel.FONT_WIDTH)) / 2, (pyxel.height / 2 - pyxel.FONT_HEIGHT), "VICTORY", 12)
            return

        if self.currentGameState == GameState.LOSE:
            # pyxel.text(pyxel.width//3, pyxel.height//3, "YOU LOSE", 8)
            pyxel.text((pyxel.width - (len("YOU DIED") * pyxel.FONT_WIDTH)) / 2, (pyxel.height / 2 - pyxel.FONT_HEIGHT), "YOU DIED", 8)
            return