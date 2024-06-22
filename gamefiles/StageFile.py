from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from random import choice

from gamefiles.Cell import Cell
from gamefiles.PlayerController import PlayerController
from gamefiles.EnemyController import EnemyController

from objects.Brick import Brick
from objects.Stone import Stone
from objects.Water import Water
from objects.Forest import Forest
from objects.Home import Home
from objects.Mirror import Mirror

from gamefiles.Signal import Signal


'''
STAGE FORMAT:
    NOTE: Please see resources/stages/_TEST.txt for a complete example

    object discriminator
    separated by | for each column
    separated by NEWLINE for each row
    
    Object Disriminators:
        " " OR str(1 to 15) -- empty cell
            - numbers are for easier counting and positioning
            - this is only for the designer, as they can put any number in any designated empty cell regardless of where it is
        "Brick"
        "CrackedBrick"
        "Stone"
        "Water"
        "Forest"
        "Home"
        "MirrorNE" -- mirror, facing northeast side
        "MirrorSE" -- mirror, facing southeast side
        "Spawn" -- empty cell, but it's where the player spawns
        "EnemySpawn" -- empty cell, but it's where an enemy could (possibly) spawn
    
    EXAMPLE: (5x5 grid for brevity)

     | | | | 
    Spawn|2|3|4|5
    MirrorNE| | | | 
     | |Home| | 
     | | | |Water
     |EnemySpawn|EnemySpawn| | 

    NOTE: on the left and right edges, there must still be a space if you wish to specify an empty cell !!
    NOTE: Please see resources/stages/_TEST.txt for a complete example

'''



'''
Stage interface for GameField use

Stage
    onLifeChanged: Signal[[int], None]
    onStageGenerated: Signal[[], None]

    init()

    generate_stage(filename: str)
        - defaults:
            - remaining enemy spawns: 5
            - enemy spawn interval: 3.5

    get_lives() -> int
    set_lives(lives: int)
    get_spawn() -> tuple[int, int]
    get_player() -> PlayerController
    spawn_player()
        - fails if lives <= 0

    get_enemies()
    get_total_enemy_count()
        - enemies on screen + remaining enemy spawns
    spawn_enemy()
    
    update(frame_count: int)
        - called every game loop
        - handles periodic enemy spawning
    cleanup()
        - called before new stage is generated
'''

class Stage():
    _enemySpawns: list[tuple[int, int]]
    _homes: list[Home]
    _enemies: list[EnemyController]
    def __init__(self, game: GameField):
        self.game = game

        self.onLifeChanged = Signal[[int], None](game)
        self.onStageGenerated = Signal[[], None](game)
    
    def init(self):
        self.generate_stage("_empty")

    def generate_stage(self, filename: str, lives: int = 2):
        spawnpoint: tuple[int, int] | None = None

        self._enemySpawns = []
        self._homes = []

        stage = open(f"resources/stages/{filename}.txt", "r")
        lines = stage.readlines()
        for r in range(len(lines)):

            line = lines[r].rstrip("\n")
            objects = line.split("|")

            for c in range(len(objects)):
                
                id = objects[c]
                Cell(self.game, c, r)

                if id in [str(x) for x in range(1, 16)] or id == " ":
                    continue
                if id == "Brick":
                    Brick(self.game, c, r)
                elif id == "CrackedBrick":
                    Brick(self.game, x=c, y=r, cracked=True)
                elif id == "Stone":
                    Stone(self.game, c, r)
                elif id == "Water":
                    Water(self.game, c, r)
                elif id == "Forest":
                    Forest(self.game, c, r)
                elif id == "Home":
                    self._homes.append(Home(self.game, c, r))

                elif id == "MirrorNE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="northeast")

                elif id == "MirrorSE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="southeast")
                
                elif id == "Spawn":
                    if spawnpoint:
                        raise ValueError("Stage cannot have more than one player spawnpoint!")
                    spawnpoint = (c, r)
                elif id == "EnemySpawn":
                    self._enemySpawns.append((c,r))
                else:
                    raise ValueError("Invalid stage file!")
                    
        if spawnpoint is None:
            raise ValueError("Please specify player spawn!")
        
        self._lives = lives
        self._remainingEnemySpawns = 1
        self._enemies = []

        self._spawnpoint = spawnpoint
        # placeholder
        self._player = PlayerController(self.game, self.game.tankFactory.tank(x=0,y=0,team="player",tank_type="Normal"))

        self._maxEnemies = self.get_total_enemy_count()
        self._powerupSpawned = False

        self._lastEnemySpawnFrame = 0
        self._enemySpawnInterval = 3.5

        self.spawn_player()

        self.onStageGenerated.fire()

    def get_lives(self):
        return self._lives
    
    def set_lives(self, lives: int):
        self._lives = lives

    def get_homes(self):
        return self._homes
    
    def get_spawn(self):
        return self._spawnpoint
    
    def get_player(self) -> PlayerController:
        return self._player
    
    def spawn_player(self):
        if self.get_lives() <= 0:
            return
        self.get_player().tank.destroy()

        (x, y) = self._spawnpoint
        player = PlayerController(
            game=self.game,
            tank=self.game.tankFactory.tank(x=x, y=y, team="player", tank_type="Normal")
        )
        self._player = player
        
        def decrease_life():
            self.set_lives(self.get_lives()-1)
            self.onLifeChanged.fire(self.get_lives())
        self._decrease_life_listener = decrease_life
        self._player.tank.onDestroy.add_listener(decrease_life)
    
    def get_enemies(self):
        return self._enemies
    
    def get_enemy_spawns(self):
        return self._enemySpawns

    def get_total_enemy_count(self) -> int:
        return len(self.get_enemies()) + (self._remainingEnemySpawns if len(self.get_enemy_spawns()) > 0 else 0)

    def spawn_enemy(self):
        if self._remainingEnemySpawns <= 0:
            return
        if len(self._enemySpawns) == 0:
            return
        self._remainingEnemySpawns -= 1

        enemy_spawns = self.get_enemy_spawns()
        coords = choice(enemy_spawns)
        x, y = coords

        enemy = EnemyController(
            game=self.game,
            tank=self.game.tankFactory.tank(x=x, y=y, team="enemy", tank_type=choice(self.game.tankFactory.get_tank_types()))
        )
        def remove_enemy():
            self._enemies.remove(enemy)
        enemy.tank.onDestroy.add_listener(remove_enemy)
        self._enemies.append(enemy)

    def update(self, frame_count: int):
        # enemy spawn
        if frame_count > (self._lastEnemySpawnFrame + (self.game.FPS * self._enemySpawnInterval)):
            self._lastEnemySpawnFrame = frame_count
            self.spawn_enemy()

        # powerup spawn
        if not self._powerupSpawned:
            if self.get_total_enemy_count() < self._maxEnemies / 2:

                empty_cells: list[Cell] = []
                for r in range(self.game.r):
                    for c in range(self.game.c):
                        cell = self.game[r, c]
                        if len(cell.get_objects()) == 0:
                            empty_cells.append(cell)

                if len(empty_cells) > 0:
                    
                    chosen_cell = choice(empty_cells)
                    self.game.powerupFactory.powerup(
                        x=chosen_cell.x,
                        y=chosen_cell.y,
                        powerup_type=choice(self.game.powerupFactory.get_powerup_types()))
                    self._powerupSpawned = True
    
    def cleanup(self):
        self.get_player().tank.onDestroy.remove_listener(self._decrease_life_listener)
        [obj.destroy() for r in range(self.game.r) for c in range(self.game.c) for obj in self.game[c, r].get_objects()]


