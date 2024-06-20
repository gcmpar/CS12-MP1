import pyxel

from pyxelgrid import PyxelGrid
from gamefiles.Cell import Cell
from gamefiles.PhysicsManager import PhysicsManager
from gamefiles.Renderer import Renderer

from gamefiles.StageFile import Stage

from misc.util import GameState


'''
GameField
    FPS: int
    physics: PhysicsManager
    renderer: Renderer
    stage: stage


'''

class GameField(PyxelGrid[Cell]):
    def __init__(self, fps: int, r: int = 15, c: int = 15, dim: int = 16):
        super().__init__(r, c, dim=dim)
        self.FPS = fps
        self.run(title="Battle Tanks Bootleg:tm:", fps=fps)

    def init(self):
        # internals
        self.physics = PhysicsManager(self)
        self.renderer = Renderer(self)
        self.stage = Stage(self)
        pyxel.load("resources/spritesheet.pyxres")

        self.currentGameState = GameState.READY
    
    def start_stage(self, stage: int):
        self.currentStage = stage
        self.stage.generate_stage("stage"+str(self.currentStage))
        self.currentGameState = GameState.ONGOING

    def next_stage(self):
        if self.currentStage == 3:
            return
        self.start_stage(self.currentStage + 1)
        

    
    def update(self):
        # 0 game state
        if self.currentGameState == GameState.READY:
            if pyxel.btn(pyxel.KEY_0):
                self.start_stage(1)
            return
        elif self.currentGameState != GameState.ONGOING:
            if self.currentGameState == GameState.WIN:
                if pyxel.btn(pyxel.KEY_2):
                    self.next_stage()
                    return

            if pyxel.btn(pyxel.KEY_1):
                self.start_stage(self.currentStage)
            elif pyxel.btn(pyxel.KEY_0):
                self.start_stage(1)

            return
            

        
        if self.stage.get_player().tank.is_destroyed():
            self.currentGameState = GameState.LOSE
        elif self.stage.get_total_enemies() == 0:
            self.currentGameState = GameState.WIN
        

        # 1 input handling
        self.stage.get_player().update(pyxel.frame_count)

        # 2 physics
        self.physics.update(pyxel.frame_count)

        # 3 game objects
        [obj.main_update(pyxel.frame_count) for r in range(self.r) for c in range(self.c) for obj in self[c, r].get_objects()]

        # 4 enemy
        enemies = self.stage.get_enemies()
        for enemy in enemies:
            enemy.update(pyxel.frame_count)
        
        # 5 stage
        self.stage.update(pyxel.frame_count)

    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        self.renderer.draw_cell(pyxel.frame_count, i, j, x, y)

    def pre_draw_grid(self):
        self.renderer.pre_draw_grid()
        
    def post_draw_grid(self):
        self.renderer.post_draw_grid()
