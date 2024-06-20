
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
    def __init__(self, fps: int, r: int = 15, c: int = 15, dim: int = 16):
        super().__init__(r, c, dim=dim)
        self.FPS = fps
        self.run(title="Battle Tanks Bootleg:tm:", fps=fps)
        

    def init(self) -> None:
        # internals
        self.physics = PhysicsManager(self)
        self.renderer = Renderer(self)
        self.StageFile = Stage(game=self)
        pyxel.load("resources/spritesheet.pyxres")

        
        self.currStage = 1
        self.StageFile.generate_stage(self.currStage, 2)
        self.currentGameState = GameState.READY


    def update(self) -> None:
        # 0 game state
        if self.currentGameState == GameState.READY:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.currentGameState = GameState.ONGOING
            else:
                return

        if self.currentGameState == GameState.ONGOING:
            
                
            # 1 input handling
            self.StageFile.player.update(pyxel.frame_count)
            # for player in self.StageFile.player:
            #     player.update(pyxel.frame_count)
            #     if player.tank.is_destroyed():
            #         self.StageFile.player.remove(player)

            # 2 physics
            self.physics.update(pyxel.frame_count)

            # 3 game objects
            [obj.main_update(pyxel.frame_count) for r in range(self.r) for c in range(self.c) for obj in self[c, r].get_objects()]

            # TODO 4 enemy
            for enemy in self.StageFile.enemies:
                enemy.update(pyxel.frame_count)
                if enemy.tank.is_destroyed():
                    self.StageFile.enemies.remove(enemy)
                
            self.StageFile.update(pyxel.frame_count)

            if not self.StageFile.enemies and self.StageFile.remainingEnemies == 0:
                self.StageFile.player.tank.destroy()
                if self.currStage == len(self.StageFile.Layouts):
                    self.currentGameState = GameState.WIN
                else:
                    self.currStage += 1
                    self.StageFile.generate_stage(self.currStage, self.StageFile.Lives)
                    self.currentGameState = GameState.READY
                return

            if self.StageFile.player.tank.is_destroyed():
            # if not self.StageFile.player:
                if self.StageFile.Lives == 0:
                    self.currentGameState = GameState.LOSE
                    return
                # else:
                #     print(self.StageFile.Lives)
        
        
        


    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        self.renderer.update_cell(pyxel.frame_count, i, j, x, y)

    def pre_draw_grid(self) -> None:
        # background
        pyxel.rect(0, 0, self.c*self.dim, self.r*self.dim, 0)

    def post_draw_grid(self) -> None:
        pyxel.text(0,0,f"Lives: {self.StageFile.Lives}",12)

        if self.currentGameState == GameState.WIN:
            # pyxel.text(pyxel.width//2, pyxel.height//2, "YOU WIN", 12)
            pyxel.text((pyxel.width - (len("VICTORY") * pyxel.FONT_WIDTH)) / 2, (pyxel.height / 2 - pyxel.FONT_HEIGHT), "VICTORY", 12)
            pyxel.text((pyxel.width - (len("Press 1 to Restart") * pyxel.FONT_WIDTH)) / 2, (pyxel.height / 2), "Press 1 to Restart", 11)
            if pyxel.btnp(pyxel.KEY_1):
                pyxel.rect(0, 0, self.c*self.dim, self.r*self.dim, 0)
                self.currStage = 1
                self.StageFile.generate_stage(self.currStage, 2)
                self.currentGameState = GameState.READY
            return

        if self.currentGameState == GameState.LOSE:
            # pyxel.text(pyxel.width//3, pyxel.height//3, "YOU LOSE", 8)
            pyxel.text((pyxel.width - (len("YOU DIED") * pyxel.FONT_WIDTH)) / 2, (pyxel.height / 2 - pyxel.FONT_HEIGHT), "YOU DIED", 8)
            pyxel.text((pyxel.width - (len("Press 1 to Restart") * pyxel.FONT_WIDTH)) / 2, (pyxel.height / 2), "Press 1 to Restart", 11)
            if pyxel.btnp(pyxel.KEY_1):
                pyxel.rect(0, 0, self.c*self.dim, self.r*self.dim, 0)
                self.currStage = 1
                self.StageFile.generate_stage(self.currStage, 2)
                self.currentGameState = GameState.READY
            return