from __future__ import annotations

from typing import TYPE_CHECKING

from random import choice

from gamefiles.Cell import Cell
from gamefiles.PlayerController import PlayerController
from gamefiles.EnemyController import EnemyController

from objects.Tank import Tank
from objects.Brick import Brick
from objects.Stone import Stone
from objects.Mirror import Mirror
from objects.Water import Water

if TYPE_CHECKING:
    from gamefiles.GameField import GameField


class Stage():
    def __init__(self, game: GameField):
        
        self.FPS = game.FPS
        self.game = game
        self.Layouts: dict[int, list[list[str]]] = {
            1: [
            ["EnemySpawn","None","None","None","None","None","None","None","None","None","None","None","None","None","EnemySpawn"],
            ["None","Stone","Stone","Stone","None","None","Brick","Brick","Brick","None","None","Stone","Stone","Stone","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","Stone","None"],
            ["None","None","None","None","mSE","None","None","None","None","None","mNE","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","Stone","None"],
            ["None","Stone","None","Brick","Brick","Brick","None","None","None","Brick","Brick","Brick","None","Stone","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["Water","Water","Water","Water","None","None","Water","Stone","Water","None","None","Water","Water","Water","Water"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","Stone","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","Stone","None"],
            ["None","None","None","None","mNE","None","None","None","None","None","mSE","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","Spawn","None","None","None","None","None","Stone","None"],
            ["None","Stone","Stone","Stone","None","None","Brick","Brick","Brick","None","None","Stone","Stone","Stone","None"],
            ["None","None","None","None","None","None","Brick","None","Brick","None","None","None","None","None","None"],
            ],
            2: [
            ["EnemySpawn","None","None","None","None","None","None","None","None","None","None","None","None","None","EnemySpawn"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","Spawn","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ]
        }
    def get_layout(self, stageLevel) -> list[list[str]]:
        return self.Layouts[stageLevel]
    
    def generate_stage(self, stageLevel, Lives):
        self.currStage = self.get_layout(stageLevel)
        
        self.Lives = Lives

        self.enemies = list[EnemyController]()
        self.remainingEnemies = 0
        self.enemySpawns = []
        for r in range(len(self.currStage)):
            for c in range(len(self.currStage[0])):
                Cell(self.game, x=c, y=r)
                if self.currStage[r][c] == "None":
                    pass

                if self.currStage[r][c] == "Stone":
                    Stone(self.game, x=c, y=r)

                if self.currStage[r][c] == "Brick":
                    Brick(self.game, x=c, y=r)

                if self.currStage[r][c] == "Water":
                    Water(self.game, x=c, y=r)
                
                if self.currStage[r][c] == "mNE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="northeast")

                if self.currStage[r][c] == "mSE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="southeast")

                if self.currStage[r][c] == "Spawn":
                    self.Spawnpoint = (c,r)

                    self.player = (PlayerController(
                        game=self,
                        tank=Tank(game=self.game, x=c, y=r, team="player",
                                
                                health=1,
                                movement_speed=5,
                                fire_rate=1,
                            )
                        )
                    )
                    
                if self.currStage[r][c] == "EnemySpawn":
                    self.enemySpawns.append((c,r))

                    self.enemies.append(EnemyController(
                        game=self,
                        tank=Tank(game=self.game, x=c, y=r, team="enemy",
                                
                                health=1,
                                movement_speed=5,
                                fire_rate=1,
                            )
                        )
                    )
        
    
    def update(self, frame_count: int): 
        if len(self.enemies) < 2 and self.remainingEnemies > 0:
            c,r = choice(self.enemySpawns)

            self.enemies.append(EnemyController(
                        game=self,
                        tank=Tank(game=self.game, x=c, y=r, team="enemy",
                                
                                health=1,
                                movement_speed=5,
                                fire_rate=1,
                            )
                        )
                    )
            
            self.remainingEnemies -= 1

        if self.player.tank.is_destroyed() and self.Lives > 0:
            c,r = self.Spawnpoint

            self.player = (PlayerController(
                        game=self,
                        tank=Tank(game=self.game, x=c, y=r, team="player",
                                
                                health=1,
                                movement_speed=5,
                                fire_rate=1,
                            )
                        )
                    )
