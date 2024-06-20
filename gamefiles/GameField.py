from collections.abc import Callable

import pyxel

from pyxelgrid import PyxelGrid
from gamefiles.Cell import Cell

from gamefiles.PhysicsManager import PhysicsManager
from gamefiles.Renderer import Renderer
from gamefiles.SoundManager import SoundManager

from gamefiles.StageFile import Stage
from misc.util import GameState
from misc.Signal import Signal

from objects.GameObject import GameObject


class GameField(PyxelGrid[Cell]):
    def __init__(self, fps: int, r: int = 15, c: int = 15, dim: int = 16):
        super().__init__(r, c, dim=dim)
        self.FPS = fps
        self.run(title="Battle Tanks Bootleg:tm:", fps=fps)

    def init(self):
        # internals
        self._signalDestroyQueue = list[Callable[[], None]]()

        self.physics = PhysicsManager(self)
        self.renderer = Renderer(self)
        self.sounds = SoundManager(self)
        pyxel.load("resources/spritesheet.pyxres")

        self.currentGameState = GameState.READY
        self.onObjectAdded = Signal[[GameObject], None](self)

        self.stage = Stage(self)
        self.physics.init()
        self.renderer.init()
        self.sounds.init()
    
    def start_stage(self, stage: int, lives: int):
        self.stage.cleanup()

        self.currentStage = stage
        self.stage.generate_stage(str(self.currentStage), lives)
        self.currentGameState = GameState.ONGOING

        # TEST
        from objects.Tank import Tank
        t1 = Tank(self, 2, 8, "enemy", 5, 2, 1)
        t2 = Tank(self, 2, 2, "enemy", 5, 2, 1)
        t1.turn("north")
        t2.turn("south")
        t1.start_moving()
        t2.start_moving()

    def next_stage(self):
        self.start_stage(
            stage=self.currentStage + 1 if self.currentStage < 3 else 3,
            lives=self.stage.get_lives()
            )
        

    
    def update(self):
        # 0 game state
        if self.currentGameState == GameState.READY:
            if pyxel.btn(pyxel.KEY_0):
                self.start_stage(stage=1, lives=2)
            return
        elif self.currentGameState != GameState.ONGOING:
            if self.currentGameState == GameState.WIN:
                if pyxel.btn(pyxel.KEY_1):
                    self.next_stage()
                    return
            elif pyxel.btn(pyxel.KEY_0):
                self.start_stage(stage=1,lives=2)

            return

        # 1 input handling
        player = self.stage.get_player()
        if player.tank.is_destroyed():
            if pyxel.btn(pyxel.KEY_R):
                self.stage.spawn_player()

        if not player.tank.is_destroyed():
            player.update(pyxel.frame_count)

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

        # 6 process signal destroy
        [f() for f in self._signalDestroyQueue]
        self._signalDestroyQueue = []

        # 7 check game state
        if self.stage.get_lives() == 0 or self.stage.get_home().is_destroyed():
            self.currentGameState = GameState.LOSE
        elif self.stage.get_total_enemy_count() == 0:
            self.currentGameState = GameState.WIN

    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        self.renderer.draw_cell(pyxel.frame_count, i, j, x, y)

    def pre_draw_grid(self):
        self.renderer.pre_draw_grid()
        
    def post_draw_grid(self):
        self.renderer.post_draw_grid()


    # ---------------------------------
    # INTERNAL
    def queue_signal_destroy(self, f: Callable[[], None]):
        self._signalDestroyQueue.append(f)
