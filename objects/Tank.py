from __future__ import annotations
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from objects.GameField import GameField
    
from objects.GameObject import GameObject
from objects.Bullet import Bullet
from objects.util import Orientation, Team

'''
Tank
    team: Team

    orientation: "north" // "south" // "east" // "west"
        - where the tank is currently facing
    
    speed: int
        - how many cells the tank can move per second
    fire_rate: int
        - how many bullets the tank can fire per second
        
    move(ori: Orientation) -> bool
        - change pos according to orientation
        - limited by speed
        - returns True if moved to cell successfully
    
    fire()
        - fires bullet

'''

class Tank(GameObject):
    orientation: Orientation
    def __init__(self, game: GameField, x: int, y: int, ori: Orientation = "east", team: Team = "enemy"):
        super().__init__(game, x, y)
        self._last_move_frame = 0
        self._last_fire_frame = 0

        self.team = team
        self.orientation = ori
        self.speed = 5
        self.fire_rate = 1


    def move(self, ori: Orientation) -> bool:
        # movement cap
        if pyxel.frame_count < (self._last_move_frame + (self.game.FPS / self.speed)):
            return False
        self._last_move_frame = pyxel.frame_count
        self.orientation = ori

        x_move = 1 if ori == "east" else -1 if ori == "west" else 0
        y_move = 1 if ori == "south" else -1 if ori == "north" else 0

        # update
        return self.move_to(self.get_cell().x + x_move, self.get_cell().y + y_move)
    
    def fire(self):
        # fire cap
        if pyxel.frame_count < (self._last_fire_frame + (self.game.FPS / self.fire_rate)):
            return
        self._last_fire_frame = pyxel.frame_count

        ori = self.orientation
        x_move = 1 if ori == "east" else -1 if ori == "west" else 0
        y_move = 1 if ori == "south" else -1 if ori == "north" else 0

        Bullet(
            game=self.game,
            x=self.get_cell().x + x_move,
            y=self.get_cell().y + y_move,
            owner=self,
            ori=ori,
            )

    def collided_with(self, other: GameObject):
        if isinstance(other, Bullet):
            self.destroy()
        