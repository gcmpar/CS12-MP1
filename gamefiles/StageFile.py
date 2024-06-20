from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from random import choice

from gamefiles.Cell import Cell
from gamefiles.PlayerController import PlayerController
from gamefiles.EnemyController import EnemyController

from objects.Tank import Tank
from objects.Brick import Brick
from objects.Stone import Stone
from objects.Water import Water
from objects.Mirror import Mirror

from misc.Signal import Signal


'''
Stage
    onLifeChanged: Signal[[int], None]
    onStageGenerated: Signal[[], None]

    generate_stage(filename: str)

    get_lives() -> int
    set_lives(lives: int)

    get_player() -> PlayerController
    spawn_player()

    get_enemies()
    get_total_enemy_count()
    spawn_enemy()
    
    update(frame_count: int)
'''

class Stage():
    _enemySpawns: list[tuple[int, int]]
    _enemies: list[EnemyController]
    def __init__(self, game: GameField):
        self.game = game

        self.onLifeChanged = Signal[[int], None](game)
        self.onStageGenerated = Signal[[], None](game)

        self.generate_stage("_empty")

    def generate_stage(self, filename: str, lives: int = 2):
        spawnpoint: tuple[int, int] | None = None

        self._enemySpawns = []
        self._enemies = []
        self._lives = lives

        self._lastEnemySpawnFrame = 0
        self._enemySpawnInterval = 0.35

        stage = open("resources/stages/"+filename+".txt", "r")
        lines = stage.readlines()
        for r in range(len(lines)):

            line = lines[r].rstrip("\n")
            objects = line.split("|")

            for c in range(len(objects)):
                
                id = objects[c]
                Cell(self.game, c, r)

                if id == " ":
                    continue
                if id == "Brick":
                    Brick(self.game, x=c, y=r)
                elif id == "CrackedBrick":
                    Brick(self.game, x=c, y=r, cracked=True)
                elif id == "Stone":
                    Stone(self.game, x=c, y=r)
                elif id == "Water":
                    Water(self.game, x=c, y=r)

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
                    
        if spawnpoint == None:
            raise ValueError("Please specify player spawn!")
        
        self._spawnpoint = spawnpoint
        self.spawn_player()
        self.spawn_enemy()

        self.onStageGenerated.fire()

    def get_lives(self):
        return self._lives
    
    def set_lives(self, lives: int):
        self._lives = lives

    def get_player(self):
        return self._player
    
    def spawn_player(self):
        if self.get_lives() <= 0:
            return
        player = (PlayerController(
                game=self.game,
                tank=Tank(game=self.game, x=self._spawnpoint[0], y=self._spawnpoint[1], team="player",
                        health=1,
                        movement_speed=5,
                        fire_rate=1,
                    )
                )
            )
        self._player = player
        
        def decrease_life():
            self.set_lives(self.get_lives()-1)
            self.onLifeChanged.fire(self.get_lives())
        self._decrease_life_listener = decrease_life
        self._player.tank.onDestroy.add_listener(decrease_life)
    
    def get_enemies(self):
        return self._enemies
    
    def get_total_enemy_count(self) -> int:
        return len(self.get_enemies()) + len(self._enemySpawns)

    def spawn_enemy(self):
        if len(self._enemySpawns) == 0:
            return

        coords = choice(self._enemySpawns)
        self._enemySpawns.remove(coords)
        x, y = coords
        enemy = EnemyController(
            game=self.game,
            tank=Tank(game=self.game, x=x, y=y, team="enemy",
                    
                    health=1,
                    movement_speed=5,
                    fire_rate=1,
                )
            )
        def remove_enemy():
            self._enemies.remove(enemy)
        enemy.tank.onDestroy.add_listener(remove_enemy)
        self._enemies.append(enemy)

    def update(self, frame_count: int):
        if len(self.get_enemies()) < 2 and len(self._enemySpawns) > 0:
            if frame_count > (self._lastEnemySpawnFrame + (self.game.FPS / self._enemySpawnInterval)):
                self._lastEnemySpawnFrame = frame_count
                self.spawn_enemy()
    
    def cleanup(self):
        self.get_player().tank.onDestroy.remove_listener(self._decrease_life_listener)
        [obj.destroy() for r in range(self.game.r) for c in range(self.game.c) for obj in self.game[c, r].get_objects()]


