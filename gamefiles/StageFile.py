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



class Stage():
    _player: PlayerController | None
    _enemySpawns: list[tuple[int, int]]
    _enemies: list[EnemyController]
    _lastEnemySpawnFrame: int
    def __init__(self, game: GameField):
        self.game = game

        self._player = None
        self._enemySpawns = []
        self._enemies = []
        self._lastEnemySpawnFrame = 0
        self._enemySpawnInterval = 0.35

    def generate_stage(self, filename: str):
        player: PlayerController | None = None
        self._enemySpawns = []
        self._enemies = []
        self._lastEnemySpawnFrame = 0

        stage = open("resources/stages/"+filename+".txt", "r")
        lines = stage.readlines()
        for r in range(len(lines)):
            line = lines[r].rstrip("\n")

            objects = line.split("|")
            for c in range(len(objects)):
                id = objects[c]
                Cell(self.game, c, r)
                print(id, "Yeah")
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
                    if player:
                        raise ValueError("Stage cannot have more than one player spawn!")
                    player = (PlayerController(
                        game=self.game,
                        tank=Tank(game=self.game, x=c, y=r, team="player",
                                health=1,
                                movement_speed=5,
                                fire_rate=1,
                            )
                        )
                    )
                elif id == "EnemySpawn":
                    self._enemySpawns.append((c,r))
                else:
                    raise ValueError("Invalid stage file!")
                    
        if player == None:
            raise ValueError("Please specify player spawn!")
        
        self._player = player
        self.spawn_enemy()

    def get_player(self):
        if self._player is None:
            raise ValueError("Player somehow does not exist. Stage may not have been generated.")
        return self._player
    
    def get_enemies(self):
        return self._enemies

    def get_remaining_spawns(self) -> int:
        return len(self._enemySpawns)
    
    def get_total_enemies(self) -> int:
        return len(self.get_enemies()) + self.get_remaining_spawns()

    def spawn_enemy(self):
        if self.get_remaining_spawns() == 0:
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
        if len(self.get_enemies()) < 2 and self.get_remaining_spawns() > 0:
            if frame_count > (self._lastEnemySpawnFrame + (self.game.FPS / self._enemySpawnInterval)):
                self._lastEnemySpawnFrame = frame_count
                self.spawn_enemy()


