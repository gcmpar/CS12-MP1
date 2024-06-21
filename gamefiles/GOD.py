from __future__ import annotations
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from misc.util import GameState

from objects.Tank import Tank

'''
Singleton for Debug mode and cheat codes
CHEAT CODES (Hold CTRL key):
    L
        - extra life, respawns player and continues game even if win/lose
    K
        - smites all enemies and automatically wins the game

God
    game: GameField

    init()
    update()

'''

class God:
    def __init__(self, game: GameField):
        self.game = game

        self._lifeDebounce = False
    
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

                    stage.get_player().tank.destroy()
                    stage.set_lives(current_lives+1)
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