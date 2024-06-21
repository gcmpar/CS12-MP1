from __future__ import annotations
from typing import TYPE_CHECKING
from random import choice

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.Cell import Cell

from misc.util import GameState

from objects.Tank import Tank

'''
Singleton for Debug mode and cheat codes
CHEAT CODES (Hold CTRL key):
    L
        - extra life, respawns player and continues game even if win/lose
    K
        - smites all enemies present on field
    Z
        - automatically win the game
    X
        - spawn a random powerup

God
    game: GameField

    init()
    update()

'''

class God:
    def __init__(self, game: GameField):
        self.game = game

        self._lifeDebounce = False
        self._powerupDebounce = False
    
    def init(self):
        pass

    def update(self):
        if self.game.currentGameState == GameState.READY:
            return
        
        if pyxel.btn(pyxel.KEY_CTRL):
            if pyxel.btn(pyxel.KEY_L):
                if not self._lifeDebounce:
                    self._lifeDebounce = True

                    stage = self.game.stage
                    current_lives = stage.get_lives()
                    
                    stage.set_lives(current_lives+1)
                    if stage.get_player().tank.is_destroyed():
                        stage.spawn_player()

                    homes = stage.get_homes()
                    for home in homes:
                        if home.is_destroyed():
                            homes.remove(home)

                    self.game.currentGameState = GameState.ONGOING
            else:
                self._lifeDebounce = False
            
            if pyxel.btn(pyxel.KEY_K):
                for r in range(self.game.r):
                    for c in range(self.game.c):
                        cell = self.game[r, c]
                        for obj in cell.get_objects():

                            if isinstance(obj, Tank):
                                if obj.team == "enemy":
                                    obj.destroy()

            if pyxel.btn(pyxel.KEY_Z):
                self.game.currentGameState = GameState.WIN
            
            if pyxel.btn(pyxel.KEY_X):
                if not self._powerupDebounce:
                    self._powerupDebounce = True
                    empty_cells: list[Cell] = []
                    for r in range(self.game.r):
                        for c in range(self.game.c):
                            cell = self.game[r, c]
                            if len(cell.get_objects()) == 0:
                                empty_cells.append(cell)

                    if len(empty_cells) > 0:
                        
                        chosen_cell = choice(empty_cells)
                        self.game.powerupFactory.powerup(x=chosen_cell.x, y=chosen_cell.y, powerup_type=choice(self.game.powerupFactory.get_powerup_types()))
            else:
                self._powerupDebounce = False