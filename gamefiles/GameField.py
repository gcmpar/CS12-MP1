from collections.abc import Callable

import pyxel

from pyxelgrid import PyxelGrid
from gamefiles.Cell import Cell

from gamefiles.PhysicsManager import PhysicsManager
from gamefiles.Renderer import Renderer
from gamefiles.SoundManager import SoundManager
from gamefiles.GOD import God

from gamefiles.TankFactory import TankFactory
from gamefiles.PowerupFactory import PowerupFactory

from gamefiles.StageFile import Stage
from misc.util import GameState
from gamefiles.Signal import Signal

from objects.GameObject import GameObject


'''
the World class

GameField
    FPS: int

    physics: PhysicsManager
    renderer: Renderer
    sounds: SoundManager
    stage: Stage
    tankFactory: TankFactory

    currentStage: int
    currentGameState: GameState
    onObjectAdded: Signal[[GameObject], None]
        - fired for any GameObject creation
    onStateChanged: Signal[[GameState], None]
    onPreObjectUpdate: Signal[[int], None]
    onPostObjectUpdate: Signal[[int], None]
    onPostPhysicsUpdate: Signal[[int], None]
    
    start_stage(stage: int, lives: int)
        - cleans the game field up
        - loads the stage with path "resources/stages/{stage}.txt"
        - sets GameState to ONGOING
    
    next_stage()
        - calls start_stage for currentStage + 1, or stays in same stage if file does not exist
        - also passes in lives value of previous stage via stage.get_lives()
    
    update()
        - the main game loop
        - ORDER:
            - pre-loop GameState check (returns if not ONGOING)
                - also checks button inputs for game restarting/next stage

            - inputs (PlayerController updates)
            - EnemyController updates
            - stage-specific updates
            - GameObject updates
            - physics
            - signal destroy processing

            - GameState check (WIN/LOSE)

    ---------------------------------
    # INTERNALS

    queue_signal_destroy(f: Callable[[], None])
        - all Signals call this function to tag them for cleanup
        - Signal destroy is handled asynchronously (at the end of the frame in game loop)
        - this is to let Signals still fire for at most 1 frame after GameObject is destroyed

'''

class GameField(PyxelGrid[Cell]):
    def __init__(self, fps: int, r: int = 15, c: int = 15, dim: int = 16):
        super().__init__(r, c, dim=dim)
        self.FPS = fps
        self.run(title="Battle Tanks Bootleg:tm:", fps=fps)

    def init(self):
        # internals
        for r in range(self.r):
            for c in range(self.c):
                Cell(self, r, c)
        self._signalDestroyQueue = list[Callable[[], None]]()
        self._restartDebounce = False

        self.stage = Stage(self)
        self.physics = PhysicsManager(self)
        self.renderer = Renderer(self)
        self.sounds = SoundManager(self)
        self.tankFactory = TankFactory(self)
        self.powerupFactory = PowerupFactory(self)
        self.GOD = God(self)
        pyxel.load("resources/resource.pyxres")

        self.currentStage = 1
        self._currentGameState = GameState.READY
        self.onObjectAdded = Signal[[GameObject], None](self)
        self.onStateChanged = Signal[[GameState], None](self)
        self.onPreObjectUpdate = Signal[[int], None](self)
        self.onPostObjectUpdate = Signal[[int], None](self)
        self.onPostPhysicsUpdate = Signal[[int], None](self)

        # init
        self.set_game_state(GameState.READY)
        self.stage.init()
        self.physics.init()
        self.renderer.init()
        self.sounds.init()
        self.GOD.init()
    
    def get_game_state(self) -> GameState:
        return self._currentGameState
    def set_game_state(self, state: GameState):
        if state == self._currentGameState:
            return
        self._currentGameState = state
        self.onStateChanged.fire(state)
    
    def start_stage(self, stage: int, lives: int, remaining_enemy_spawns: int, copy_modifiers: bool):
        self.set_game_state(GameState.GENERATING)

        was_destroyed = self.stage.get_player().tank.is_destroyed()
        modifiers = [mod.copy() for mod in self.stage.get_player().tank.get_modifiers() if mod.stageTransferrable]
        self.stage.cleanup()

        self.currentStage = stage
        self.stage.generate_stage(str(self.currentStage), lives=lives, remaining_enemy_spawns=remaining_enemy_spawns)

        if copy_modifiers and not was_destroyed:
            player_tank = self.stage.get_player().tank
            for mod in modifiers:
                    mod.owner = player_tank
                    player_tank.add_modifier(mod)

        self.renderer.init_stage()
        self.sounds.init_stage()
        self.set_game_state(GameState.ONGOING)
        
        # PHYSICS TEST (can remove this ig)
        # from objects.Stone import Stone
        # Stone(self, 1, 2)
        # t1 = self.tankFactory.tank(2, 4, "enemy", "Armored")
        # t2 = self.tankFactory.tank(3, 2, "enemy", "Armored")
        # t1.set_orientation("north")
        # t2.set_orientation("west")
        # t1.start_moving()
        # t2.start_moving()

    def next_stage(self):
        # Change this for more stages ig
        stage_number = self.currentStage + 1 if self.currentStage < 3 else 3
        remaining_enemy_spawns = 1 if stage_number == 1 \
                                else 3 if stage_number == 2 \
                                else 5
        self.start_stage(
            stage=stage_number,
            lives=self.stage.get_lives(),
            remaining_enemy_spawns=remaining_enemy_spawns,
            copy_modifiers=True
            )
        

    
    def update(self):
        # -1 GOD
        self.GOD.update()

        # 0 game state
        if pyxel.btn(pyxel.KEY_1):
            if not self._restartDebounce:
                self._restartDebounce = True
                self.start_stage(stage=1,lives=2,remaining_enemy_spawns=1,copy_modifiers=False)
                return
        else:
            self._restartDebounce = False
        
        current_state = self.get_game_state()
        if current_state == GameState.READY:
            return
        elif current_state == GameState.WIN or current_state == GameState.LOSE:
            if current_state == GameState.WIN:
                if pyxel.btn(pyxel.KEY_2):
                    self.next_stage()
                    return
            return
        elif current_state != GameState.ONGOING:
            return

        if self.stage.get_lives() == 0 or True in {h.is_destroyed() for h in self.stage.get_homes()}:
            self.set_game_state(GameState.LOSE)
        elif self.stage.get_total_enemy_count() == 0:
            self.set_game_state(GameState.WIN)

        # 1 input handling
        player = self.stage.get_player()
        if player.tank.is_destroyed():
            if pyxel.btn(pyxel.KEY_R):
                self.stage.spawn_player()

        if not player.tank.is_destroyed():
            player.update(pyxel.frame_count)
        
        # 2 enemy
        enemies = self.stage.get_enemies()
        for enemy in enemies:
            enemy.update(pyxel.frame_count)

        # 3 stage
        self.stage.update(pyxel.frame_count)

        self.onPreObjectUpdate.fire(pyxel.frame_count)

        # 4 game objects
        [obj.main_update(pyxel.frame_count) for r in range(self.r) for c in range(self.c) for obj in self[r, c].get_objects()]

        self.onPostObjectUpdate.fire(pyxel.frame_count)

        # 5 physics
        self.physics.update(pyxel.frame_count)

        self.onPostPhysicsUpdate.fire(pyxel.frame_count)

        # 6 process signal destroy
        [f() for f in self._signalDestroyQueue]
        self._signalDestroyQueue = []

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
