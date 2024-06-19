from __future__ import annotations

from typing import TYPE_CHECKING

from gamefiles.Cell import Cell
from gamefiles.PlayerController import PlayerController

from objects.Tank import Tank
from objects.Brick import Brick
from objects.Stone import Stone
from objects.Mirror import Mirror

if TYPE_CHECKING:
    from gamefiles.GameField import GameField


class Stage():
    def __init__(self, game: GameField):
        
        self.game = game
        self.stage1 = [
            ["Spawn","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","Stone","Stone","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","mSE","None","None","None","None","None","None","None","mNE","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","mNE","None","None","None","None","None","None","None","mSE","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","None","None","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","Stone","Stone","Stone","None","None","None","None","None","None","None","None","None","None","None"],
            ["None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"],
                ]
    
    def generate_stage(self, currStage):
        for r in range(len(currStage)):
            for c in range(len(currStage[0])):
                Cell(self.game, x=c, y=r)
                if currStage[r][c] == "None":
                    pass

                if currStage[r][c] == "Stone":
                    Stone(self.game, x=c, y=r)

                if currStage[r][c] == "Brick":
                    Brick(self.game, x=c, y=r)
                
                if currStage[r][c] == "mNE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="northeast")

                if currStage[r][c] == "mSE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="southeast")

                if currStage[r][c] == "Spawn":
                    self.player = PlayerController(game=self.game, tank=Tank(game=self.game, x=c, y=r, team="player", ori="north"))

